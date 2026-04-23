# Common Issues Reference Guide

Quick reference for the most frequent bugs and their solutions.

## 1. Data Not Refreshing

**Symptoms**:
- KPI cards show old data after refreshing
- Chart doesn't update after applying filters
- Latest data not appearing

**Root Causes & Solutions**:

### Cause A: Store State Not Updating

**Diagnosis**:
```javascript
// In browser console
const dataStore = useDataStore()
console.log('Store data:', dataStore.kpiData)
console.log('Loading:', dataStore.loading)
```

**Fix**:
```javascript
// Force refresh
dataStore.fetchKpiData()
```

### Cause B: Component Not Re-rendering

**Diagnosis**: Data changed in store but UI didn't update

**Fix**: Ensure reactive refs are used correctly
```javascript
// ✅ Correct
const kpiData = computed(() => dataStore.kpiData)

// ❌ Wrong
const kpiData = dataStore.kpiData  // Not reactive
```

### Cause C: API Cached Response

**Diagnosis**:
```bash
# Check Network tab → Headers → Cache-Control
```

**Fix**: Add cache-busting parameter
```javascript
// services/api.js
export const getKpiData = () => {
  return axios.get(`/api/kpi?t=${Date.now()}`)
}
```

---

## 2. Filters Not Working

**Symptoms**:
- Selecting institution/team doesn't change data
- "清空筛选" button doesn't reset filters

**Root Causes & Solutions**:

### Cause A: FilterStore Not Triggering Data Fetch

**Diagnosis**:
```javascript
// Check if filter action calls data refresh
const filterStore = useFilterStore()
console.log('Active institution:', filterStore.activeInstitution)

// After setting filter, check if data action was called
```

**Fix**: Ensure FilterPanel calls dataStore action
```javascript
// In FilterPanel.vue
const handleInstitutionChange = (value) => {
  filterStore.setInstitution(value)
  dataStore.fetchFilteredData()  // Must call this
}
```

### Cause B: API Not Receiving Filter Parameters

**Diagnosis**: Check Network tab → Request URL should include filter params

**Expected**: `/api/kpi?institution=重庆分公司&team=团队A`

**Fix**: Verify API service passes params correctly
```javascript
// services/api.js
export const getKpiData = (filters) => {
  return axios.get('/api/kpi', { params: filters })
}
```

---

## 3. Charts Not Displaying

**Symptoms**:
- Blank chart area
- Console error: "Cannot read property 'getContext' of null"
- Chart shows briefly then disappears

**Root Causes & Solutions**:

### Cause A: Chart Container Has Zero Height

**Diagnosis**:
```javascript
// In ChartView.vue onMounted
console.log('Container:', chartRef.value)
console.log('Width:', chartRef.value.offsetWidth)
console.log('Height:', chartRef.value.offsetHeight)  // Should NOT be 0
```

**Fix**: Set explicit height
```vue
<div ref="chartRef" style="height: 400px"></div>
```

### Cause B: ECharts Not Initialized

**Diagnosis**: Check console for ECharts errors

**Fix**: Ensure proper initialization sequence
```javascript
import * as echarts from 'echarts'

onMounted(() => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)
  chart.setOption(chartOptions)
})
```

### Cause C: Data Format Mismatch

**Diagnosis**: ECharts expects specific data structure

**Fix**: Transform API data to ECharts format
```javascript
// Backend returns: [{ date: '2025-01-01', value: 1000 }]
// ECharts needs: { xAxis: ['2025-01-01'], series: [{ data: [1000] }] }

const chartData = computed(() => {
  const rawData = dataStore.chartData || []
  return {
    xAxis: { data: rawData.map(d => d.date) },
    series: [{ data: rawData.map(d => d.value) }]
  }
})
```

---

## 4. API Errors (500/404)

**Symptoms**:
- Network tab shows red requests
- Console error: "Request failed with status code 500"

**Root Causes & Solutions**:

### Cause A: Backend Not Running

**Diagnosis**:
```bash
lsof -i :5000  # Should show python process
```

**Fix**:
```bash
cd backend
python3 api_server.py
```

### Cause B: CSV File Missing

**Diagnosis**: Check backend logs
```bash
tail -f backend/backend.log
# Look for: FileNotFoundError: 车险清单_2025年10-11月_合并.csv
```

**Fix**:
```bash
# Verify file exists
ls -la *.csv

# If missing, rebuild from Excel
cd backend
python3 -c "from data_processor import DataProcessor; DataProcessor().scan_and_process_new_files()"
```

### Cause C: Pandas Processing Error

**Diagnosis**: Backend log shows:
```
KeyError: '保费'
TypeError: unsupported operand type(s)
```

**Fix**: Check CSV column names match code expectations
```python
# In data_processor.py
df.columns = df.columns.str.strip()  # Remove whitespace
required_cols = ['保单号', '业务员姓名', '总保费', '签单日期']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")
```

---

## 5. CORS Errors

**Symptoms**:
- Console error: "Access-Control-Allow-Origin"
- Network request fails with CORS policy error

**Root Causes & Solutions**:

### Cause: Flask-CORS Not Configured

**Diagnosis**: Check if Flask-CORS is enabled
```python
# In api_server.py
from flask_cors import CORS
CORS(app)  # Should be present
```

**Fix**: Ensure CORS is imported and applied

### Advanced: Specific Origins

If deploying to production:
```python
CORS(app, origins=['https://your-domain.com'])
```

---

## 6. Slow Performance

**Symptoms**:
- API takes > 3 seconds to respond
- UI freezes when applying filters
- Browser becomes unresponsive

**Root Causes & Solutions**:

### Cause A: Large CSV File

**Diagnosis**:
```bash
ls -lh 车险清单_2025年10-11月_合并.csv
# If > 50MB, consider optimization
```

**Fix**: Load data in chunks or filter at database level

### Cause B: Pandas Row Iteration

**Diagnosis**: Check for `.iterrows()` in code

**Fix**: Use vectorized operations
```python
# ❌ SLOW
for index, row in df.iterrows():
    df.at[index, 'new_col'] = row['old_col'] * 2

# ✅ FAST
df['new_col'] = df['old_col'] * 2
```

### Cause C: Too Many API Calls

**Diagnosis**: Network tab shows 10+ requests per action

**Fix**: Batch requests or cache responses
```javascript
// Use debounce for filter changes
import { debounce } from 'lodash'

const debouncedFetch = debounce(() => {
  dataStore.fetchKpiData()
}, 300)
```

---

## 7. Build Failures

**Symptoms**:
- `npm run build` fails
- Missing dependencies errors

**Root Causes & Solutions**:

### Cause A: Node Version Mismatch

**Diagnosis**:
```bash
node -v  # Should be 18+
```

**Fix**: Update Node.js or use nvm
```bash
nvm install 18
nvm use 18
```

### Cause B: Corrupted node_modules

**Fix**:
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 8. Validation Warnings

**Symptoms**:
- Yellow warning banner: "发现 X 名业务员在数据中存在但在映射文件中未找到"

**Root Causes & Solutions**:

### Cause: Staff Mapping Outdated

**Fix**: Update `业务员机构团队归属.json`
1. Export latest staff list from HR system
2. Convert to JSON format
3. Replace old mapping file
4. Restart backend

---

## 9. Memory Leaks

**Symptoms**:
- Browser memory usage keeps increasing
- Tab crashes after prolonged use

**Root Causes & Solutions**:

### Cause: ECharts Instance Not Disposed

**Fix**: Clean up charts on unmount
```javascript
// In ChartView.vue
onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
})
```

---

## 10. Deployment Issues

**Symptoms**:
- Works locally but fails on server
- Cannot access from external network

**See**: [deployment-and-ops Skill](../deployment-and-ops/SKILL.md) for detailed solutions

**Quick checks**:
```bash
# Is backend running?
ps aux | grep api_server

# Is port accessible?
curl http://localhost:5000/api/latest-date

# Check firewall
sudo iptables -L  # Linux
```

---

## Quick Diagnostic Flowchart

```
Problem?
├─ UI not updating
│  ├─ Check Console for errors
│  ├─ Check Vue DevTools → Store state
│  └─ Force refresh: dataStore.fetch...()
│
├─ API failing
│  ├─ Check Network tab → Status code
│  ├─ Check backend logs: tail -f backend/backend.log
│  └─ Test with curl
│
├─ Chart not showing
│  ├─ Check container height > 0
│  ├─ Check chartData format
│  └─ Check ECharts console errors
│
└─ Performance slow
   ├─ Check CSV file size
   ├─ Profile Pandas operations
   └─ Check Network waterfall
```

---

**Last Updated**: 2025-11-08
**Maintained By**: Claude Code AI Assistant
