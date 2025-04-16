import os
import openai
import subprocess

# ✅ Manually Set Azure OpenAI API Key (Replace with your actual key)
API_KEY = "4Pht6BC341X3qO5C4AEN2X2EqsJar5I2y6QtFlhDVw67wrPXCk3tJQQJ99BDACYeBjFXJ3w3AAABACOGTZdU"  # 🔴 WARNING: Do NOT expose this in public repositories!

# ✅ Ensure correct Azure OpenAI endpoint
BASE_URL = "https://jenkins-openai.openai.azure.com/"  

# ✅ Confirm correct deployment name from Azure OpenAI Studio
DEPLOYMENT_NAME = "gpt-4o-mini"  # 🔹 Update if different

# ✅ Ensure correct API version (check Azure OpenAI portal)
API_VERSION = "2023-12-01-preview"  # 🔹 Update if needed

# ✅ Initialize OpenAI client
openai_client = openai.AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=BASE_URL,
    api_version=API_VERSION
)

# ✅ Define repository path
repo_path = r"C:\\Users\\MTL1027\\Downloads\\llyods-demo-backend" # 🔹 Change this to your repo path
jenkinsfile_path = os.path.join(repo_path, "Jenkinsfile")

# ✅ Define prompt for AI (modified for .jar deployment)
prompt = """Generate a Jenkinsfile with the following conditions:
- The response should contain only valid Jenkinsfile syntax.
- Do NOT include Markdown formatting like 'groovy' or 'sh' at the start or end.
- The response should start directly with 'pipeline {'.
- The pipeline should have three stages: Build, Test, and Deploy.
- Use 'bat' instead of 'sh' for Windows compatibility.
- The Build stage should run 'mvn clean package'.
- The Test stage should run 'mvn test'.
- Declare environment variables globally using the 'environment' block:
  - RESOURCE_GROUP = credentials('RESOURCE_GROUP')
  - WEB_APP_NAME = credentials('WEB_APP_NAME')
- In the Deploy stage, authenticate with Azure using service principal credentials stored as separate Jenkins secrets:
  - Use 'withCredentials' to load three secret text values:
    - AZURE_CLIENT_ID → variable: CLIENT_ID
    - AZURE_CLIENT_SECRET → variable: CLIENT_SECRET
    - AZURE_TENANT_ID → variable: TENANT_ID
  - Use a 'bat' block to run:
    - 'az login --service-principal --username %CLIENT_ID% --password %CLIENT_SECRET% --tenant %TENANT_ID%'
    - Then deploy using:
      - 'az webapp deploy --resource-group %RESOURCE_GROUP% --name %WEB_APP_NAME% --src-path target\\*.jar --type jar'
- Use Windows-style environment variable syntax (e.g., %VARIABLE%) inside bat commands.
- Do not use Groovy string interpolation (like ${}) inside the bat command.


"""



try:
    print("⏳ Generating Jenkinsfile using Azure OpenAI...")

    # ✅ Correct the request format for Azure OpenAI
    response = openai_client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )

    # ✅ Extract Jenkinsfile content
    jenkinsfile_content = response.choices[0].message.content.strip()

    # ✅ Replace 'sh' with 'bat' (if not already done by the AI)
    jenkinsfile_content = jenkinsfile_content.replace('sh ', 'bat ')

    # ✅ Ensure repository exists
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"❌ Repository path not found: {repo_path}")

    # ✅ Save the Jenkinsfile
    with open(jenkinsfile_path, "w") as file:
        file.write(jenkinsfile_content + "\n")

    print(f"✅ Jenkinsfile created at {jenkinsfile_path}")

    # ✅ Git commit and push changes
    print("⏳ Adding and committing Jenkinsfile...")

    subprocess.run(["git", "-C", repo_path, "add", "Jenkinsfile"], check=True)

    # ✅ Check if there are any changes before committing
    status_output = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"], capture_output=True, text=True)

    if status_output.stdout.strip():
        subprocess.run(["git", "-C", repo_path, "commit", "-m", "Auto-generated Jenkinsfile"], check=True)
        subprocess.run(["git", "-C", repo_path, "push", "origin", "main"], check=True)
        print("🚀 Jenkinsfile successfully pushed to GitHub!")
    else:
        print("⚠️ No changes detected. Skipping commit and push.")

except Exception as e:
    print(f"❌ Error generating or pushing Jenkinsfile: {e}")
