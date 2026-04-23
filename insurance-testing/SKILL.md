---
name: insurance-testing
description: Detailed testing standards for persistence, service, and controller layers
---

# When to use

Use this skill when creating or modifying tests in this project.

# Core principles

1. Use AAA structure in every test.
2. Keep Act phase to one line in unit tests.
3. Keep tests deterministic (no hidden time/env/network dependencies).
4. Use descriptive method names that state scenario and expected behavior.
5. Pick the narrowest useful test type:
    - unit tests for pure business logic,
    - slice tests for web/repository concerns,
    - full integration only when cross-layer wiring matters.

# Testing stack by layer

- Unit: JUnit 5 + Mockito.
- Controller slice: `@WebMvcTest` + `MockMvc`.
- Persistence/integration: `@SpringBootTest` or `@DataJpaTest` with in-memory DB.
- Optional: Testcontainers for infrastructure fidelity when in-memory DB is insufficient.

# Persistence tests

Applies to repository/integration-style tests.

1. Use transactional rollback per test class (`@Transactional` + `@Rollback`) to avoid side effects.
2. Seed stable data via SQL scripts when needed (`src/test/resources/sql/` + `@Sql`).
3. After write operations (`create/update/delete`), call `EntityManager.flush()` before assertions.
4. Verify DB state independently from ORM behavior whenever possible:
    - `JdbcTestUtils.countRowsInTable`
    - `JdbcTestUtils.countRowsInTableWhere`
5. Keep shared constants and entity factories in a central `InstanceProvider`.
6. Prefer fixed IDs/emails/names in test constants that match SQL seeds.
7. File naming: `<Entity>RepositoryTest`.

### Persistence example

```java
@Transactional
@Rollback
@SpringBootTest
class UserRepositoryTest {

    private static final String EMAIL = "test@example.com";

    @PersistenceContext
    private EntityManager em;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    void testCreate() {
        // Arrange
        int before = JdbcTestUtils.countRowsInTable(jdbcTemplate, "users");

        // Act
        User user = userRepository.create(EMAIL, "secret", "John", "Doe");
        em.flush();

        // Assert
        assertEquals(before + 1, JdbcTestUtils.countRowsInTable(jdbcTemplate, "users"));
        assertNotNull(user);
    }
}
```

# Service tests

Pure unit tests (no Spring context).

1. Use Mockito JUnit integration (`@ExtendWith(MockitoExtension.class)`).
2. Mock collaborators with `@Mock`.
3. Build subject with `@InjectMocks`.
4. Stub only what the scenario needs.
5. Use `assertThrows` for failure scenarios.
6. File naming: `<Service>ImplTest`.

### Service example

```java
@ExtendWith(MockitoExtension.class)
class UserServiceImplTest {

    private static final long USER_ID = 1L;

    @InjectMocks
    private UserServiceImpl userService;

    @Mock
    private UserRepository userRepository;

    @Test
    void testFindByIdExistingUser() {
        // Arrange
        when(userRepository.findById(USER_ID)).thenReturn(Optional.of(new User()));

        // Act
        Optional<User> result = userService.findById(USER_ID);

        // Assert
        assertTrue(result.isPresent());
    }

    @Test
    void testFindByIdNonExisting() {
        // Arrange
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

        // Act
        Optional<User> result = userService.findById(1L);

        // Assert
        assertFalse(result.isPresent());
    }
}
```

# Controller tests

Use Mockito helpers or slice tests based on scope.

1. For request logic/helpers, prefer Mockito unit tests.
2. For endpoint contract and MVC behavior, use `@WebMvcTest` + `MockMvc`.
3. Mock auth/request objects as needed.
4. If entity IDs are generated and lack setters, use local test helpers (reflection-based if required).
5. File naming: `<Entity>ControllerTest`.

### Controller helper pattern

```java
private User createUserWithId(String email, Long id) throws Exception {
    User user = new User(email);
    Field idField = User.class.getDeclaredField("id");
    idField.setAccessible(true);
    idField.set(user, id);
    return user;
}
```

Keep small helper methods (`createUserWithId`, `createMockAuthentication`, etc.) inside the test class to reduce
duplication and improve readability.

# Test review checklist

- [ ] AAA shape is explicit.
- [ ] Act phase is one line (unit tests).
- [ ] Assertions validate outcome and important side effects.
- [ ] Collaborator interactions are verified only when behaviorally relevant.
- [ ] Test names and fixtures clearly express intent.
- [ ] Repository tests flush before asserting persisted state.
- [ ] Controller tests cover validation/error paths for request boundaries.
