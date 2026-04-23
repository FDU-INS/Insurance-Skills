---
name: insurance-aggregator
description: "Страховой агрегатор: архитектура, калькуляторы, адаптеры СК, CRM, лояльность, реферальная программа. Обучен на InsSmart, Sravni Labs, Polis.Online, Pampadu. Use when: страхование, ОСАГО, КАСКО, ВЗР, ипотечное, агрегатор, калькулятор, котировки, страховой агент, полис, СК, комиссия."
---

# Insurance Aggregator — Полная экспертиза

Этот skill содержит ВСЕ знания, необходимые для создания продакшн-уровня страхового агрегатора — B2B/B2C платформы для расчёта, сравнения и оформления страховых полисов.

Обучен на реальных данных 4 B2B-платформ (InsSmart, Sravni Labs, Polis.Online, Pampadu), потребительском Sravni.ru и 20+ open-source проектах.

---

## Часть 1: Архитектура платформы

### 1.1 Три роли

```
┌─────────────────────────────────────────────────────────────┐
│                     INSURANCE PLATFORM                       │
├─────────────┬──────────────────────┬────────────────────────┤
│ Пользователь│      Агент           │    Админ               │
│ (B2C)       │      (B2B)           │    (Internal)          │
├─────────────┼──────────────────────┼────────────────────────┤
│ Поиск полиса│ Калькулятор          │ Управление СК          │
│ Сравнение   │ Результаты + комиссия│ Комиссионные правила   │
│ Покупка     │ Оформление           │ Управление агентами    │
│ Мои полисы  │ CRM клиентов         │ Отчёты (глобальные)    │
│ Напоминания │ Баланс / Финансы     │ Лояльность (настройки) │
│             │ Отчёты               │ Модерация              │
│             │ Реферальная программа│                        │
│             │ Инструменты продаж   │                        │
│             │ Лояльность (уровни)  │                        │
└─────────────┴──────────────────────┴────────────────────────┘
```

### 1.2 Модули платформы

| Модуль | Приоритет | Описание |
|---|---|---|
| **Калькуляторы** | P0 | Multi-step wizard для каждого продукта, автозаполнение |
| **Quote Engine** | P0 | Параллельные запросы к адаптерам СК, кеширование, ранжирование |
| **Результаты** | P0 | Список предложений: цена, СК, рейтинг, покрытие, комиссия агента |
| **Оформление полиса** | P0 | Checkout: оплата, подтверждение, генерация полиса |
| **Мои полисы** | P0 | Активные, истекающие, архив, статусы |
| **CRM клиентов** | P0 | Карточка клиента: ФИО, полисы, расчёты, контакты |
| **Баланс / Финансы** | P0 | Начисления, списания, вывод средств |
| **Черновики** | P1 | Автосохранение незавершённых расчётов |
| **Отчёты** | P1 | Продажи, воронка, Excel export, группировка |
| **Реферальная программа** | P1 | Генерация ссылок, метрики, типы |
| **Лояльность** | P2 | 5 уровней, квартальный расчёт, бонусные комиссии |
| **Планировщик** | P2 | Календарь: ДР, пролонгации, events |
| **Инструменты продаж** | P2 | Виджеты, визитки, контент, обучение |
| **Управление агентами** | P2 | Подагенты, иерархия, квоты |
| **Справочники СК** | P2 | Рейтинги, отзывы, claim settlement ratio |

### 1.3 Жизненный цикл полиса

```
Черновик → Расчёт → Выбор → Оформление → Оплата → Активный → Пролонгация
                                                        ↓
                                                    Истекающий (за 30 дней)
                                                        ↓
                                                    Истёкший (архив)
                                                        ↓
                                              Claims (при страховом случае)
```

---

## Часть 2: Продуктовый каталог

### 2.1 Страховые продукты

#### ОСАГО (обязательное, регулируется ЦБ РФ)
- **Формула**: ТБ × КТ × КБМ × КВС × КО × КМ × КС × КП × КН
- **Коэффициенты**:
  - ТБ: 2746-4942₽ (коридор ЦБ для категории B)
  - КТ: 0.6-2.1 (территориальный, по 88 регионам)
  - КБМ: 0.46-3.92 (бонус-малус, 14 классов, проверка АИС РСА)
  - КВС: 0.83-1.87 (возраст × стаж, матрица)
  - КО: 1.0 (ограниченный список) / 1.94 (без ограничений)
  - КМ: 0.6-1.6 (мощность двигателя)
  - КС: 0.5-1.0 (период использования)
  - КП: 0.2-1.0 (период страхования)
  - КН: 1.0-1.5 (нарушения)
- **Автозаполнение**: по госномеру → марка, модель, год, мощность
- **КБМ**: автоматическая проверка через АИС РСА (Edge Function)

#### КАСКО (добровольное, устанавливается СК)
- **Примерная стоимость**: 4-8% от стоимости авто
- **Базовая формула**: стоимость_авто × базовая_ставка × К_возраст_авто × К_регион × К_франшиза × К_стаж × К_КБМ
- **Доп.факторы**: кол-во ключей, срок владения, КАСКО-убытки за год, кредитный авто, автозапуск, праворульный
- **Покрытие**: полное КАСКО, мини-КАСКО (ограниченные риски), КАСКО + GAP

#### Ипотечное (обязательное для ипотеки)
- **Типы покрытия**: Имущество (конструктив), Жизнь заёмщика, Титул
- **Стоимость**: 0.15-0.5% от остатка кредита
- **Факторы**: банк-кредитор, остаток, год постройки, тип объекта, пол, возраст, здоровье
- **Особенность**: банк диктует минимальный набор покрытий

#### ВЗР / Travel
- **Стоимость**: ~90-300₽/день
- **Факторы**: страна, дни, возраст, сумма покрытия
- **Опции**: спорт, беременность, хронические заболевания
- **Quick-picks стран**: Грузия, Таиланд, Шенген, Китай, Вьетнам, Турция

#### НС (Несчастный случай)
- **Типы**: На период / На год
- **Опции**: Для лагеря, Для спорта
- **Простая форма**: возраст, даты, кол-во

#### Антиклещ
- **Стоимость**: 340-390₽
- **Поля**: возраст, дата начала (на год)
- **Референс**: Зетта 340₽, СберСтрах 360₽, ВСК 390₽, Ингосстрах 390₽

#### ИФЛ (Имущество физлиц)
- **Покрытие**: Отделка/ремонт, Мебель/техника, Ответственность перед соседями
- **Фильтры**: газ, деревянные перекрытия, аренда
- **Стоимость**: от 1,800₽/год (квартира)

#### Титул
- **Период**: годовой
- **Стоимость**: зависит от рыночной стоимости имущества (300K-50M₽)

### 2.2 Дополнительные услуги

| Услуга | Описание |
|---|---|
| Техосмотр | Запись на ТО: город, категория ТС, станция |
| ДКП | Бесплатный шаблон договора купли-продажи |
| Проверка ОСАГО | По VIN — актуальность полиса |
| Подбор ипотеки | 20+ банков, сравнение условий |
| Оценка имущества | Для страхования / ипотеки |
| Биржа ОСАГО | 100+ исполнителей, аукционная модель |

---

## Часть 3: Multi-Step Wizard — калькулятор

### 3.1 Архитектура визарда

```typescript
interface WizardStep {
  id: string
  title: string
  fields: FieldConfig[]
  validation: ZodSchema
  autoFill?: AutoFillConfig  // автозаполнение (госномер → данные ТС)
  skipCondition?: (data: FormData) => boolean  // пропустить шаг
}

interface FieldConfig {
  name: string
  label: string
  type: 'text' | 'select' | 'date' | 'number' | 'checkbox' | 'toggle' | 'phone' | 'masked'
  mask?: string           // '#### ######' для паспорта
  required: boolean
  defaultValue?: unknown
  options?: SelectOption[] // для select
  autoComplete?: AutoCompleteConfig
  dependsOn?: string      // показать только если заполнено другое поле
  copyFrom?: string       // «Скопировать из собственника»
}
```

### 3.2 ОСАГО — Golden Standard (7 шагов)

**Шаг 1: Данные ТС**
```
fields:
  - gosNumber: { type: 'masked', mask: 'A ### AA ###', autoComplete: vehicleLookup }
  - noGosNumber: { type: 'checkbox', label: 'Госномер отсутствует' }
  - withTrailer: { type: 'checkbox', label: 'ТС с прицепом' }
  - category: { type: 'select', options: ['B', 'A', 'C', 'D', 'BE', ...], default: 'B' }
  - purpose: { type: 'select', options: ['Личная', 'Такси', 'Учебная', 'Перевозка'], default: 'Личная' }
  - brand: { type: 'select', autoFilled: true }
  - model: { type: 'select', dependsOn: 'brand', autoFilled: true }
  - year: { type: 'number', min: 1970, max: currentYear, autoFilled: true }
  - power: { type: 'number', suffix: 'л.с.', autoFilled: true }
  - powerKw: { type: 'number', suffix: 'кВт' }
  - vin: { type: 'masked', mask: 'XXXXXXXXXXXXXXXXX' }
  - docType: { type: 'select', options: ['ПТС', 'СТС', 'ЭПТС'] }
  - docSeries: { type: 'masked', mask: '## ##' }
  - docNumber: { type: 'masked', mask: '######' }
  - docDate: { type: 'date' }
```

**Шаг 2: Собственник**
```
fields:
  - ownerType: { type: 'select', options: ['ФЛ', 'ИП', 'ЮЛ'], default: 'ФЛ' }
  - lastName: { type: 'text', required: true }
  - firstName: { type: 'text', required: true }
  - middleName: { type: 'text' }
  - birthDate: { type: 'date', required: true }
  - passportSeries: { type: 'masked', mask: '## ##' }
  - passportNumber: { type: 'masked', mask: '######' }
  - passportDate: { type: 'date' }
  - address: { type: 'text', autoComplete: addressSuggest }
```

**Шаг 3: Страхователь**
```
fields:
  - isOwner: { type: 'checkbox', label: 'Является собственником', default: true }
  // если isOwner=false → показать те же поля что у собственника
  - lastName, firstName, middleName, birthDate, passport*, address (skipIf: isOwner)
```

**Шаг 4: Водители**
```
fields:
  - multiDrive: { type: 'toggle', label: 'Без ограничений (мультидрайв)' }
  // если multiDrive=false → показать список водителей
  - drivers[]: {
      lastName, firstName, middleName: { type: 'text' }
      birthDate: { type: 'date' }
      licSeries: { type: 'masked', mask: '## ##' }
      licNumber: { type: 'masked', mask: '######' }
      licDate: { type: 'date' }  // дата выдачи ВУ
      expStart: { type: 'date' } // дата начала стажа
      foreignLic: { type: 'checkbox', label: 'Иностранное ВУ' }
      prevLic: { type: 'checkbox', label: 'Указать предыдущее ВУ (для переноса КБМ)' }
      prevLicSeries, prevLicNumber: { dependsOn: 'prevLic' }
      copyFromOwner: { type: 'button', label: 'Скопировать из собственника' }
      copyFromInsurer: { type: 'button', label: 'Скопировать из страхователя' }
    }
  - addDriver: { type: 'button', label: '+ Ещё один водитель' }
```

**Шаг 5: Данные полиса**
```
fields:
  - startDate: { type: 'date', min: tomorrow }
  - period: { type: 'select', options: ['3 мес', '6 мес', '12 мес'], default: '12 мес' }
  - greenCorridor: { type: 'checkbox', label: 'Предыдущий полис (зелёный коридор)' }
  - prevPolicyNumber: { dependsOn: 'greenCorridor', type: 'masked' }
```

**Шаг 6: Контакты**
```
fields:
  - phone: { type: 'phone', mask: '+7 (###) ###-##-##' }
  - email: { type: 'text', validation: email }
```

**Шаг 7: Подтверждение**
```
fields:
  - consentPD: { type: 'checkbox', required: true, label: 'Согласие на обработку ПД (152-ФЗ)' }
  - consentSK: { type: 'checkbox', required: true, label: 'Согласие на передачу данных СК' }
  - consentAccuracy: { type: 'checkbox', required: true, label: 'Подтверждаю достоверность' }
  - consentRules: { type: 'checkbox', required: true, label: 'Ознакомлен с правилами' }
actions:
  - saveDraft: { label: 'Сохранить черновик', variant: 'outline' }
  - calculate: { label: 'Рассчитать', variant: 'primary' }
```

### 3.3 Автозаполнение по госномеру

```
Пользователь вводит госномер (напр. А123БВ777)
  → Edge Function insurance-vehicle-lookup
    → API запрос к сервису (ГИБДД / RSA / коммерческий API)
    → Возврат: { brand, model, year, power, vin, engineVolume }
  → Форма автозаполняется
  → Пользователь проверяет и корректирует
```

### 3.4 Проверка КБМ

```
Для каждого водителя:
  → Edge Function insurance-kbm-check
    → Запрос к АИС РСА (по ФИО + ДР + ВУ)
    → Возврат: { kbmClass: number, kbmValue: number, prevInsurer: string }
  → КБМ автоподставляется в расчёт
  → Кеширование: 30 дней (КБМ меняется 1 раз/год 1 апреля)
```

---

## Часть 4: Quote Engine

### 4.1 Архитектура

```
┌─────────────┐
│  Calculator  │  ← пользователь заполнил форму
│  (Frontend)  │
└──────┬──────┘
       │ POST /api/insurance-quote
       ▼
┌──────────────┐
│ Quote Engine │  ← Edge Function
│              │
│ 1. Validate  │  ← Zod schema validation
│ 2. Cache?    │  ← Есть ли кешированный результат?
│ 3. Fan-out   │  ← Promise.allSettled([...adapters])
│ 4. Collect   │  ← Собрать ответы
│ 5. Rank      │  ← Отсортировать
│ 6. Cache     │  ← Сохранить в quote_sessions
│ 7. Return    │  ← Отдать клиенту
└──────────────┘
       │
       ├────────────┬───────────────┬──────────────┐
       ▼            ▼               ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Adapter: │ │ Adapter: │ │ Adapter: │ │ Adapter: │
│ Ингос    │ │ Альфа    │ │ СОГАЗ    │ │ Ренессанс│
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### 4.2 Adapter interface

```typescript
interface InsuranceProviderAdapter {
  code: string           // 'ingos', 'alpha', 'sogaz'
  name: string           // 'Ингосстрах'
  logo: string           // URL логотипа
  supportedProducts: ProductCode[]
  timeout: number        // ms, per-provider

  getQuote(req: QuoteRequest): Promise<ProviderQuote[]>
  purchase(req: PurchaseRequest): Promise<PurchaseResult>
  getStatus(policyId: string): Promise<PolicyStatus>
  cancel(policyId: string): Promise<CancelResult>
}

interface ProviderQuote {
  providerId: string
  providerName: string
  providerLogo: string
  providerRating: number  // 1-5
  productCode: ProductCode
  premium: number         // стоимость полиса ₽
  commission: number      // комиссия агента ₽
  commissionPercent: number
  coverage: CoverageDetails
  franchise?: number      // франшиза ₽
  paymentOptions: PaymentOption[]
  purchaseUrl?: string
  validUntil: string      // ISO date, когда котировка истекает
}
```

### 4.3 Quote Session

```typescript
interface QuoteSession {
  id: string             // uuid
  userId: string
  productCode: ProductCode
  params: QuoteRequest   // входные параметры
  paramsHash: string     // SHA-256 для дедупликации
  status: 'pending' | 'partial' | 'complete' | 'expired'
  results: ProviderQuote[]
  errors: ProviderError[]  // какие адаптеры упали
  createdAt: string
  expiresAt: string      // TTL 15 минут
}
```

### 4.4 Кеширование

```
Layer 1: React Query (staleTime: 5 min) — фронтенд
Layer 2: Quote Session (TTL: 15 min) — те же параметры → тот же результат
Layer 3: КБМ кеш (TTL: 30 days) — обновляется 1 раз/год 1 апреля
Layer 4: Vehicle кеш (TTL: 365 days) — данные ТС меняются редко
Layer 5: Provider rate кеш (TTL: 24h) — тарифы СК для аналитики
```

---

## Часть 5: Результаты расчёта

### 5.1 Карточка предложения

```
┌─────────────────────────────────────────────────┐
│ [Лого СК]  Ингосстрах           ★ 4.7 (1,234)  │
│                                                  │
│ ОСАГО                           12 450 ₽        │
│ Покрытие: стандартное                            │
│ Рейтинг надёжности: A++         Комиссия: 8%    │
│                                                  │
│ [Подробнее]  [Сравнить]  [== Оформить ==]       │
└─────────────────────────────────────────────────┘
```

### 5.2 Сортировка и фильтры

**Сортировка:**
- По цене (↑↓) — default
- По рейтингу СК (↑↓)
- По сумме покрытия (↑↓)
- По комиссии агента (↑↓) — только для агентов

**Фильтры:**
- Страховая компания (мультивыбор)
- Франшиза (0 / 10K / 20K / 50K)
- Минимальное покрытие
- Рейтинг СК (от 3.0 / от 4.0 / от 4.5)

### 5.3 Сравнение (Comparison Mode)

Пользователь выбирает 2-4 предложения → side-by-side таблица:

| Параметр | Ингосстрах | АльфаСтрахование | СОГАЗ |
|---|---|---|---|
| Цена | 12,450₽ | 11,890₽ | 13,200₽ |
| Рейтинг | 4.7 | 4.5 | 4.3 |
| Покрытие | Стандарт | Стандарт | Расширенное |
| Франшиза | 0₽ | 0₽ | 15,000₽ |
| Комиссия | 8% | 7% | 9% |
| CSR | 96% | 93% | 91% |

---

## Часть 6: CRM клиентов

### 6.1 Карточка клиента (референс: InsSmart)

```
┌─ Клиент ────────────────────────────────────┐
│ Иванов Иван Иванович                        │
│ ДР: 15.03.1985 (39 лет)                     │
│ Тел: +7 (999) 123-45-67                     │
│ Email: ivanov@example.com                    │
│                                              │
│ Авто: BMW X5, 2020, 249 л.с.                │
│ Госномер: А123БВ777                          │
│                                              │
│ ┌─ Полисы ─────────────────────────────────┐ │
│ │ ОСАГО  #XXX  до 15.09.2026  ✅ активен  │ │
│ │ КАСКО  #YYY  до 15.09.2026  ✅ активен  │ │
│ │ ОСАГО  #ZZZ  до 15.09.2025  ⛔ истёк    │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌─ Расчёты ────────────────────────────────┐ │
│ │ ОСАГО  12 предложений  15.08.2026       │ │
│ │ КАСКО  8 предложений   14.08.2026       │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ [Новый расчёт] [Пролонгация] [Редактировать]│
└──────────────────────────────────────────────┘
```

### 6.2 Пролонгации

InsSmart и Sravni Labs автоматически отслеживают полисы и показывают:
- Полисы, истекающие через 30 дней → badge «Пролонгация»
- Автоматическое уведомление агенту и клиенту
- One-click переход к расчёту нового полиса (данные предзаполнены)

### 6.3 Excel Export

Polis.Online и InsSmart поддерживают:
- Экспорт CRM в Excel
- Настройка колонок (какие поля включить)
- Фильтры (по датам, продуктам, статусам)
- Группировка (по дням, неделям, месяцам)

---

## Часть 7: Финансы и баланс

### 7.1 Модель начислений

```
Оформлен полис → Комиссия начислена на баланс агента
  → Status: 'pending' (ожидает подтверждения СК)
  → Status: 'confirmed' (СК подтвердила оплату)
  → Status: 'available' (можно вывести)
  → Status: 'withdrawn' (выведено)
```

### 7.2 Вывод средств

**InsSmart**: минимум 1,000₽, на карту / расчётный счёт
**Polis.Online**: быстрые выплаты на карту (для самозанятых)

### 7.3 Отчётность

**По периоду**: Текущий месяц, Прошлый, Квартал, Год, Все время, Custom dates
**Метрики**:
- Оформлено полисов (шт.)
- Премии (₽)
- Комиссия (₽)
- Средний чек
- Конверсия (расчёты → оформления)

---

## Часть 8: Лояльность

### 8.1 5-уровневая система (InsSmart)

```typescript
const LOYALTY_LEVELS = [
  { name: 'Новичок',         threshold: 0,       bonus: 0 },
  { name: 'Агент',           threshold: 30_000,  bonus: 5 },
  { name: 'Агент 2.0',       threshold: 75_000,  bonus: 8 },
  { name: 'Уполномоченный',  threshold: 150_000, bonus: 12 },
  { name: 'Уполномоченный+', threshold: 300_000, bonus: 15 },
] as const

// Расчёт: квартальные премии → определяют уровень
// bonus — процент надбавки к базовой комиссии
```

### 8.2 Механика

- Период оценки: **квартал** (3 месяца)
- Метрика: сумма **премий** оформленных полисов за квартал
- Повышение уровня: автоматическое при достижении порога
- Понижение уровня: если за квартал не дотянул до текущего порога → понижение на 1

---

## Часть 9: Реферальная программа

### 9.1 Модель InsSmart (2-уровневая)

```
Агент A приглашает Агент B → A получает X% от продаж B
Агент B приглашает Агент C → A получает Y% от продаж C (2-й уровень)
```

### 9.2 Модель Polis.Online (типизированные ссылки)

```typescript
type ReferralType = 
  | 'mentorship'      // Кураторство
  | 'partnership'      // Партнёрская программа  
  | 'osago'           // Оформление ОСАГО
  | 'mortgage'        // Оформление ипотечного полиса

interface ReferralLink {
  id: string
  url: string
  type: ReferralType
  name: string
  quotaPercent: number  // размер квоты %
  activations: number
  calculations: number
  policies: number      // оформлено
  createdAt: string
}
```

---

## Часть 10: Схема базы данных

### 10.1 Основные таблицы

```sql
-- Страховые продукты (справочник)
CREATE TABLE insurance_products (
  code TEXT PRIMARY KEY,           -- 'osago', 'kasko', 'mortgage', 'vzr'
  name TEXT NOT NULL,
  description TEXT,
  icon TEXT,
  sort_order INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Страховые компании (справочник)
CREATE TABLE insurance_companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL,       -- 'ingos', 'alpha', 'sogaz'
  name TEXT NOT NULL,
  logo_url TEXT,
  rating NUMERIC(2,1),             -- 1.0-5.0
  csr NUMERIC(4,1),                -- claim settlement ratio %
  is_active BOOLEAN DEFAULT true,
  supported_products TEXT[],       -- {'osago','kasko','mortgage'}
  adapter_config JSONB,           -- конфиг адаптера (timeout, base_url, etc.)
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Агенты
CREATE TABLE insurance_agents (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  loyalty_level TEXT DEFAULT 'novice', -- 'novice'|'agent'|'agent2'|'authorized'|'authorized_plus'
  quarterly_premiums NUMERIC DEFAULT 0,
  balance NUMERIC DEFAULT 0,
  referrer_id UUID REFERENCES insurance_agents(id),
  referral_code TEXT UNIQUE,
  is_self_employed BOOLEAN DEFAULT false,
  inn TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Клиенты агента (CRM)
CREATE TABLE insurance_clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES insurance_agents(id),
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  middle_name TEXT,
  birth_date DATE,
  phone TEXT,
  email TEXT,
  passport_series TEXT,
  passport_number TEXT,
  address TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ТС клиента
CREATE TABLE insurance_vehicles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID REFERENCES insurance_clients(id),
  gos_number TEXT,
  brand TEXT,
  model TEXT,
  year INTEGER,
  power INTEGER,           -- л.с.
  vin TEXT,
  doc_type TEXT,           -- 'pts', 'sts', 'epts'
  doc_series TEXT,
  doc_number TEXT,
  doc_date DATE,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Черновики расчётов
CREATE TABLE insurance_drafts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  product_code TEXT NOT NULL REFERENCES insurance_products(code),
  step INTEGER DEFAULT 1,
  form_data JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Сессии расчёта (quote sessions)
CREATE TABLE insurance_quote_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  product_code TEXT NOT NULL,
  params JSONB NOT NULL,
  params_hash TEXT NOT NULL,       -- SHA-256 для дедупликации
  status TEXT DEFAULT 'pending',   -- 'pending'|'partial'|'complete'|'expired'
  results JSONB DEFAULT '[]',
  errors JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ DEFAULT (now() + interval '15 minutes')
);

-- Полисы
CREATE TABLE insurance_policies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  agent_id UUID REFERENCES insurance_agents(id),
  client_id UUID REFERENCES insurance_clients(id),
  product_code TEXT NOT NULL,
  company_id UUID REFERENCES insurance_companies(id),
  policy_number TEXT,
  status TEXT DEFAULT 'active',    -- 'active'|'expiring'|'expired'|'cancelled'
  premium NUMERIC NOT NULL,
  commission NUMERIC DEFAULT 0,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  coverage JSONB,
  raw_data JSONB,                 -- данные формы для пролонгации
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Транзакции баланса агента
CREATE TABLE insurance_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES insurance_agents(id),
  policy_id UUID REFERENCES insurance_policies(id),
  type TEXT NOT NULL,              -- 'commission'|'bonus'|'withdrawal'|'referral'
  amount NUMERIC NOT NULL,
  status TEXT DEFAULT 'pending',   -- 'pending'|'confirmed'|'available'|'withdrawn'
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Реферальные ссылки
CREATE TABLE insurance_referral_links (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES insurance_agents(id),
  type TEXT NOT NULL,              -- 'mentorship'|'partnership'|'osago'|'mortgage'
  name TEXT,
  code TEXT UNIQUE NOT NULL,
  quota_percent NUMERIC DEFAULT 0,
  activations INTEGER DEFAULT 0,
  calculations INTEGER DEFAULT 0,
  policies INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- КБМ кеш
CREATE TABLE insurance_kbm_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_hash TEXT UNIQUE NOT NULL,  -- SHA-256(ФИО+ДР+ВУ)
  kbm_class INTEGER NOT NULL,
  kbm_value NUMERIC NOT NULL,
  prev_insurer TEXT,
  checked_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ DEFAULT (now() + interval '30 days')
);

-- Vehicle кеш
CREATE TABLE insurance_vehicle_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lookup_key TEXT UNIQUE NOT NULL,  -- госномер или VIN
  brand TEXT,
  model TEXT,
  year INTEGER,
  power INTEGER,
  vin TEXT,
  engine_volume INTEGER,
  checked_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ DEFAULT (now() + interval '365 days')
);
```

### 10.2 Индексы

```sql
CREATE INDEX idx_policies_user ON insurance_policies(user_id);
CREATE INDEX idx_policies_agent ON insurance_policies(agent_id);
CREATE INDEX idx_policies_status ON insurance_policies(status);
CREATE INDEX idx_policies_end_date ON insurance_policies(end_date);
CREATE INDEX idx_clients_agent ON insurance_clients(agent_id);
CREATE INDEX idx_transactions_agent ON insurance_transactions(agent_id);
CREATE INDEX idx_quote_sessions_hash ON insurance_quote_sessions(params_hash);
CREATE INDEX idx_quote_sessions_expires ON insurance_quote_sessions(expires_at);
CREATE INDEX idx_drafts_user ON insurance_drafts(user_id);
CREATE INDEX idx_kbm_cache_hash ON insurance_kbm_cache(driver_hash);
CREATE INDEX idx_vehicle_cache_key ON insurance_vehicle_cache(lookup_key);
CREATE INDEX idx_referral_links_agent ON insurance_referral_links(agent_id);
CREATE INDEX idx_referral_links_code ON insurance_referral_links(code);
```

### 10.3 RLS политики

```sql
-- Агент видит только своих клиентов
ALTER TABLE insurance_clients ENABLE ROW LEVEL SECURITY;
CREATE POLICY "agent_own_clients" ON insurance_clients
  FOR ALL USING (agent_id = auth.uid());

-- Пользователь видит свои полисы, агент видит полисы своих клиентов
ALTER TABLE insurance_policies ENABLE ROW LEVEL SECURITY;
CREATE POLICY "user_own_policies" ON insurance_policies
  FOR SELECT USING (user_id = auth.uid() OR agent_id = auth.uid());

-- Агент видит свои транзакции
ALTER TABLE insurance_transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "agent_own_transactions" ON insurance_transactions
  FOR SELECT USING (agent_id = auth.uid());

-- Черновики — только владелец
ALTER TABLE insurance_drafts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "user_own_drafts" ON insurance_drafts
  FOR ALL USING (user_id = auth.uid());

-- Quote sessions — только владелец
ALTER TABLE insurance_quote_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "user_own_quotes" ON insurance_quote_sessions
  FOR ALL USING (user_id = auth.uid());
```

---

## Часть 11: Edge Functions

### 11.1 insurance-quote (расчёт котировок)

```typescript
// supabase/functions/insurance-quote/index.ts
// POST: { productCode, params }
// Response: { sessionId, results: ProviderQuote[], errors: ProviderError[] }

// Логика:
// 1. Validate params (Zod)
// 2. Check cache (params_hash)
// 3. Get adapters for productCode
// 4. Promise.allSettled(adapters.map(a => a.getQuote(params)))
// 5. Collect results + errors
// 6. Rank by price ASC
// 7. Cache in quote_sessions
// 8. Return
```

### 11.2 insurance-vehicle-lookup (распознавание ТС)

```typescript
// GET: ?gosNumber=А123БВ777 или ?vin=XXXXXXXXXXXXXXXXX
// Response: { brand, model, year, power, vin, engineVolume }
// Cache: 365 days
```

### 11.3 insurance-kbm-check (проверка КБМ)

```typescript
// POST: { lastName, firstName, middleName, birthDate, licSeries, licNumber }
// Response: { kbmClass, kbmValue, prevInsurer }
// Cache: 30 days
```

### 11.4 insurance-purchase (оформление полиса)

```typescript
// POST: { quoteId, sessionId, paymentMethod }
// Response: { policyId, policyNumber, policyUrl, status }
```

---

## Часть 12: Конкурентные преимущества

### Что отличает нашу платформу от InsSmart/Sravni/Polis.Online:

| Преимущество | Описание |
|---|---|
| **Суперприложение** | Страхование = модуль экосистемы (чат + соцсеть + такси + маркетплейс) |
| **Встроенный мессенджер** | Агент ведёт клиента в чате платформы |
| **E2EE** | Паспорт, ВУ — шифрованная передача документов |
| **Нативное приложение** | Capacitor Android/iOS — push, offline, камера для документов |
| **AI-ассистент** | Claude-powered рекомендации, навигация, ответы |
| **Realtime** | Supabase Realtime — live-обновления статуса |
| **Видеозвонки с агентом** | E2EE звонки через WebRTC |

---

## Часть 13: Антипаттерны

| Антипаттерн | Как правильно |
|---|---|
| Mock-данные вместо реальных API | Sandbox от реальных СК, fallback на формулу ЦБ |
| Все поля на одной странице | Multi-step wizard (7 шагов для ОСАГО) |
| `Promise.all` для адаптеров | `Promise.allSettled` — одна СК упала → остальные ОК |
| Нет черновиков | Автосохранение каждый step |
| Нет КБМ-автопроверки | Edge Function с кешем 30 дней |
| Захардкоженные коэффициенты | Справочники в БД, обновляемые при изменении ЦБ |
| Один калькулятор на все продукты | Product-agnostic wizard engine + конфигурация per-product |
| Нет комиссии для агента | Commission engine: per-product × per-company × loyalty_level |
| Баланс без вывода | Полный финансовый модуль: начисления → подтверждение → вывод |

---

*Skill создан на основе живого тестирования 4 B2B-платформ (InsSmart, Pampadu, Sravni Labs, Polis.Online) и анализа 20+ GitHub-проектов.*
