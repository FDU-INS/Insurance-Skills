# Troubleshooting Guide

Common issues and solutions when using HealthSim.

---

## Configuration Issues

### Claude Desktop: Files Not Found

**Symptom:** Claude says it can't find HealthSim files or doesn't know about scenarios.

**Solutions:**

1. **Projects Method:**
   - Verify SKILL.md is added to your project
   - Try removing and re-adding files
   - Make sure you're in the correct project

2. **MCP Method:**
   - Check config file path:
     - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
     - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Verify JSON is valid (use jsonlint.com)
   - Check healthsim-common path is correct
   - Restart Claude Desktop after changes

### Claude Code: API Key Issues

**Symptom:** "API key not found" or authentication errors.

**Solutions:**

```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# Set for current session
export ANTHROPIC_API_KEY="your-key-here"

# Set permanently (add to ~/.zshrc or ~/.bashrc)
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### MCP Server Not Connecting

**Symptom:** Tools icon missing or MCP errors in Claude.

**Solutions:**

1. **Check Node.js:**
   ```bash
   node --version  # Should be 18+
   npm --version
   ```

2. **Test MCP server manually:**
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /path/to/healthsim-common
   # Should start without errors
   ```

3. **Check config file:**
   ```json
   {
     "mcpServers": {
       "healthsim": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/absolute/path/to/healthsim-common"
         ]
       }
     }
   }
   ```
   - Path must be absolute
   - Use forward slashes even on Windows, or escape backslashes
   - No trailing slash

---

## Generation Issues

### Output Doesn't Match Expected Schema

**Symptom:** Generated data has different structure than examples.

**Solutions:**

1. **Add data-models.md to context:**
   - Projects: Add `references/data-models.md`
   - Claude Code: Ensure you're in healthsim-common directory

2. **Be explicit in request:**
   ```
   Generate a patient following the data model schema in data-models.md
   ```

3. **Request JSON specifically:**
   ```
   Generate a patient as JSON with proper structure
   ```

### Wrong Codes or Invalid Codes

**Symptom:** ICD-10, CPT, or other codes don't exist or are incorrect.

**Solutions:**

1. **Request code validation:**
   ```
   Generate a diabetic patient with valid ICD-10-CM codes
   ```

2. **Add code-systems.md to context**

3. **Check code currency:**
   - ICD-10 codes update annually (October)
   - CPT codes update annually (January)
   - Some codes may be outdated

### Incomplete Output

**Symptom:** Claude stops mid-output or gives partial results.

**Solutions:**

1. **Request complete output:**
   ```
   Generate a complete patient record with all fields
   ```

2. **Break into smaller requests:**
   ```
   First: Generate the patient demographics
   Then: Add diagnoses and medications
   ```

3. **Claude Code: Use --print mode** for non-interactive output

### Claude Doesn't Use Specific Scenario

**Symptom:** Output doesn't follow scenario rules (e.g., diabetes scenario not used for diabetic patient).

**Solutions:**

1. **Use trigger phrases explicitly:**
   ```
   # Good - uses trigger phrase
   Generate a diabetic patient with A1C management

   # May not trigger
   Generate a patient with high blood sugar
   ```

2. **Reference the scenario:**
   ```
   Using the diabetes-management scenario, generate a patient
   ```

3. **Add the specific scenario file to context**

---

## Format Issues

### FHIR Output Not Valid

**Symptom:** FHIR resources fail validation.

**Solutions:**

1. **Request valid FHIR:**
   ```
   Generate a valid FHIR R4 Patient resource conforming to US Core profile
   ```

2. **Check resource type:**
   ```
   Generate as FHIR R4 Bundle (not FHIR R3 or STU3)
   ```

3. **Validate output:**
   - Use [FHIR Validator](https://validator.fhir.org/)
   - Check required fields are present

### HL7v2 Message Malformed

**Symptom:** HL7v2 messages don't parse correctly.

**Solutions:**

1. **Request proper delimiters:**
   ```
   Generate an HL7v2 ADT^A01 message with proper segment delimiters
   ```

2. **Check version:**
   ```
   Generate as HL7v2.5.1 (not 2.3 or 2.4)
   ```

3. **Verify MSH segment** is first and properly formatted

### X12 Formatting Issues

**Symptom:** X12 837/835 doesn't meet EDI standards.

**Solutions:**

1. **Request specific version:**
   ```
   Generate an X12 837P 5010 format claim
   ```

2. **Check segment terminators:**
   - Should use `~` as segment terminator
   - Element separator is `*`
   - Sub-element separator is `:`

---

## Performance Issues

### Slow Response Times

**Symptom:** Generation takes a long time.

**Solutions:**

1. **Reduce context:**
   - Only add necessary skill files
   - Don't add entire directories

2. **Use Claude Code --print mode:**
   ```bash
   claude --print "Generate a patient"
   ```

3. **Request simpler output:**
   - Start with JSON, convert to formats later
   - Generate fewer records at once

### Rate Limiting

**Symptom:** "Rate limit exceeded" errors.

**Solutions:**

1. **Add delays between requests**
2. **Batch requests where possible**
3. **Use lower-tier models for testing**

---

## Common Error Messages

### "I don't have information about HealthSim"

**Cause:** Skill files not in context.

**Fix:** Add SKILL.md to project or ensure MCP server is configured.

### "I'm not able to read files"

**Cause:** File access not configured.

**Fix:**
- Projects: Add files to project
- MCP: Check server configuration

### "The code XXXXX doesn't exist"

**Cause:** Invalid or outdated code.

**Fix:** Check code-systems.md or verify code with official source.

### "I can't generate that format"

**Cause:** Format skill not loaded.

**Fix:** Add relevant format file (formats/fhir-r4.md, etc.) to context.

---

## Getting Help

### Before Asking for Help

1. Check this troubleshooting guide
2. Verify your configuration
3. Try a simple test: "Generate a patient"
4. Note the exact error message

### Where to Get Help

- **GitHub Issues:** [Report bugs or request features](https://github.com/mark64oswald/healthsim-common/issues)
- **Documentation:** Check [SKILL.md](../SKILL.md) for complete reference

### What to Include in Bug Reports

1. Your environment (Claude Desktop/Claude Code, OS)
2. Configuration used (Projects or MCP)
3. The prompt you used
4. The output you received
5. The output you expected
6. Any error messages
