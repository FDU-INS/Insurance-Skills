# p3-03: Deploy the Full Agent and Start Session

## What to build

Run the full deployment pipeline and start a test session to verify everything works together.

## Tasks

1. **Run the full deploy pipeline** in order:
   ```bash
   # 1. Skills (already done in Phase 2, but re-run to verify)
   .venv/bin/python deploy/push-skills.py --all

   # 2. Agent definition
   .venv/bin/python deploy/push-agent.py

   # 3. Environment
   .venv/bin/python deploy/push-environment.py
   ```

2. **Verify `deploy/agent-ids.json`** contains all three IDs:
   ```json
   {
     "agent_id": "agent_01...",
     "agent_version": 1,
     "environment_id": "env_01..."
   }
   ```

3. **Start a test session** using the Console UI:
   - Go to `platform.claude.com`
   - Navigate to Managed Agents
   - Select the HealthSim agent
   - Start a session with the healthsim-production environment
   - Send a test message: "Hello, what can you help me with?"
   - Verify the agent responds with HealthSim-specific capabilities

4. **Also test via the CLI**:
   ```bash
   .venv/bin/python deploy/start-session.py
   ```
   Send the same test message and verify the response.

5. **Record all IDs and URLs** in `deploy/agent-ids.json` (should already be there from the scripts).

6. **Git commit**: "feat: deploy full HealthSim Managed Agent"

## Deliverables

- Full deploy pipeline executed successfully
- Agent accessible via Console UI
- Agent accessible via start-session.py CLI
- All IDs recorded
- Committed
