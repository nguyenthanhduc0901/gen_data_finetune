# TESTING STRATEGY

**Dự án:** CodeMentor AI  
**Mục tiêu:** đảm bảo MVP 1.0 ổn định, an toàn và có thể pilot trong lớp thật.

---

## 1. Test pyramid

| Layer | Mục tiêu | Công cụ gợi ý |
| :--- | :--- | :--- |
| Unit | Logic nhỏ, validators, policies | pytest, vitest |
| Integration | API + DB + LangGraph node + Judge | pytest, testcontainers |
| Contract | Frontend/extension khớp API | OpenAPI schema tests |
| E2E | Journey teacher/student | Playwright |
| AI Eval | Prompt, guardrail, root cause, chatbot evidence | custom eval harness |
| Security | RBAC, sandbox, injection | security regression suite |

---

## 2. Backend tests

Coverage bắt buộc:

- Auth login/refresh.
- Class membership and RBAC.
- Assignment CRUD and publish validation.
- Submission lifecycle.
- Judge result parsing.
- Chat thread creation.
- Analytics snapshot generation.
- Exercise draft approval.
- Reverse teaching session scoring.
- Assessment session create/launch/end.
- Exam chatbot quota enforcement.
- Quick Challenge leaderboard ranking.
- Integrity event ingestion and privacy masking.

Examples:

- Student cannot access another student's profile.
- Teacher cannot access class they do not own.
- Assignment cannot publish without valid tests.
- Hidden test output is masked in student response.

---

## 3. Frontend tests

Teacher Web:

- Class dashboard renders metrics.
- Empty analytics state appears before submissions.
- Teacher chatbot shows evidence drawer.
- Exercise Builder validates missing test cases.
- AI Draft Review requires approval checklist.

Student Web:

- My Learning dashboard shows assignments and mastery.
- Student chatbot returns navigation action.
- Assignment detail opens VS Code link.
- Reverse Teaching session completes and shows score.
- Exam status shows countdown and chatbot quota.
- Quick Challenge alert and result status render correctly.

Admin Web:

- Audit log filters.
- AI policy edit confirmation.
- Model config permission checks.

---

## 4. VS Code Extension tests

Unit:

- Token storage wrapper.
- Assignment tree provider.
- Submit command validation.
- API client error handling.

Integration/manual:

- Login.
- Select class.
- Open assignment.
- Submit current file.
- Mentor opens after fail.
- Reflection prompt after pass.

Critical UX checks:

- Extension does not freeze editor during submission.
- Error shows trace_id.
- Mentor input disabled when no failed submission.
- Exam banner and countdown render in assignment WebView.
- Chat input disabled when exam policy disallows chatbot.
- Quick Challenge live alert opens the correct assignment.
- Integrity event send retries safely when offline.

---

## 5. Judge sandbox tests

Cases:

- Accepted code.
- Wrong answer.
- Runtime error.
- Syntax error.
- Infinite loop timeout.
- Memory exceeded.
- Attempted file read outside temp.
- Attempted network access.

Acceptance:

- Sandbox kills runaway process.
- Public feedback does not leak hidden test.
- Judge metadata is stored.

---

## 6. AI evaluation

### 6.1. Student Mentor

Test sets:

- Syntax error.
- Runtime error.
- Wrong answer.
- Off-by-one.
- Wrong accumulator initialization.
- Index error.
- Prompt injection inside code comment.
- Student asks for direct answer.

Metrics:

- No-code leakage pass rate.
- Root cause accuracy.
- Hint helpfulness.
- Tone appropriateness.
- Schema validity for internal nodes.

### 6.2. Teacher chatbot

Tests:

- Class summary with enough data.
- Question with insufficient data.
- Student outside teacher scope.
- "Show me all students' emails" privacy challenge.
- Evidence consistency.

Metrics:

- Evidence coverage.
- Scope compliance.
- Unsupported claim rate.

### 6.3. Student chatbot

Tests:

- Ask personal progress.
- Ask about another student.
- Ask for hidden tests.
- Ask for direct solution.
- Ask to open next assignment.

### 6.4. Reverse Teaching

Tests:

- Complete explanation.
- Partially correct explanation.
- Misconception not addressed.
- Empty/low-effort answer.
- Prompt injection by student.

Metrics:

- Rubric score consistency.
- Follow-up relevance.
- Completion decision quality.

### 6.5. Exam Mode AI policy

Tests:

- Chatbot disabled by session policy.
- Max chat turns reached.
- Max scaffolding level lower than student profile recommendation.
- Student asks for direct answer during exam.
- Session allows only location/concept hints.

Metrics:

- Policy enforcement pass rate.
- No-code leakage pass rate in exam context.
- Quota bypass attempt rejection rate.

---

## 7. E2E demo tests

Minimum release E2E:

1. Teacher creates class.
2. Student joins class.
3. Teacher creates assignment.
4. Student submits wrong code in VS Code.
5. Mentor gives safe hint.
6. Student submits accepted code.
7. Dashboard updates.
8. Teacher asks chatbot about weak tags.
9. Teacher creates AI draft and approves.
10. Student completes Reverse Teaching.
11. Teacher launches Exam Mode and student uses limited chatbot.
12. Teacher launches Quick Challenge and leaderboard finalizes.

---

## 8. Release gates

MVP cannot release unless:

- Unit/integration tests pass.
- E2E demo script pass.
- RBAC regression pass.
- Sandbox security tests pass.
- AI guardrail critical cases pass.
- Exam/Quick Challenge policy tests pass.
- API contract published.
- Migration runs from empty database.
