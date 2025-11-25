
# Intelligent Document Querying System

An end-to-end **Generative AI RAG (Retrieval Augmented Generation)** project built on **AWS Bedrock**, **Aurora Serverless PostgreSQL**, and **Amazon S3**, with a **Streamlit** chat frontend.

This project was completed as part of the **Future AWS AI Engineer Nanodegree**.  
It shows how to turn a collection of PDF spec sheets into an **intelligent Q&A system** that can answer natural-language questions about heavy machinery.


---

## 🧪 Rubric Mapping 

The project at the begging was cloned from:
```
https://github.com/udacity/cd13926-Building-Generative-AI-Applications-with-Amazon-Bedrock-and-Python-project-solution.git
```

then it was updated & designed to satisfy the following rubric items:

1. **Base infrastructure creation**

   * Terraform apply for Stack 1 (VPC, Aurora, S3)
   * Terraform apply for Stack 2 (Knowledge Base)
   * RDS configured with extensions (`pg_extension`) and `bedrock_integration.bedrock_kb` table existing

2. **Knowledge Base Deployment and Data Sync**

   * Knowledge base visible and active in Bedrock console
   * Data source sync success from S3

3. **Python integration with Bedrock**

   * `query_knowledge_base` implemented
   * `generate_response` implemented
   * `valid_prompt` implemented and filtering undesired prompts

4. **Model Parameters**

   * `temperature_top_p_explanation.pdf` explains both in 1–2 paragraphs

5. **Bonus**

   * Sources displayed in answers (context includes source URIs)
   * Additional docs can be added to S3 to improve answers

---

## ✨ What This Project Does

At a high level, this system lets you:

1. **Upload PDF documents** (heavy machinery spec sheets) into **Amazon S3**  
2. **Index and store vector embeddings** into **Aurora Serverless PostgreSQL**  
3. Expose that data via an **AWS Bedrock Knowledge Base**  
4. Query the knowledge base from a **Streamlit chat app** using **Anthropic Claude 3 Haiku** or **(any other text generation model)** on AWS Bedrock  
5. Get answers that:
   - Use only the documentation as context
   - Include information about which files were used
   - Filter out irrelevant / unsafe questions via a prompt-validation step

---

## 🏗 High-Level Architecture

**Text description of the architecture:**

- **User** interacts with a **Streamlit chat application** running locally.
- The **chat app**:
  - Calls **AWS Bedrock Knowledge Base** (via `bedrock-agent-runtime`) to retrieve relevant document chunks from **Aurora Serverless PostgreSQL**, which was populated from **S3**.
  - Calls **AWS Bedrock Runtime** (Anthropic Claude 3 Haiku) with:
    - User question  
    - Retrieved context chunks  
- **Knowledge Base**:
  - Uses embeddings created from PDFs stored in **Amazon S3**
  - Stores and retrieves them via **Aurora PostgreSQL Serverless**
  
In short:

> User → Chat App → (Knowledge Base + Bedrock LLM) → Answer grounded in your documents

---

## ⚙️ Tech Stack

- **Cloud**
  - AWS Bedrock (Anthropic Claude 3 Haiku)
  - AWS Bedrock Knowledge Bases
  - Amazon S3
  - Amazon Aurora Serverless PostgreSQL
  - AWS Secrets Manager
  - Amazon VPC

- **Infra as Code**
  - Terraform (2 stacks: base infra + knowledge base)

- **Application**
  - Python 3.10+
  - Streamlit (chat UI)
  - Boto3 (AWS SDK for Python)

- **Environment**
  - Windows with WSL2 (Ubuntu)  
  - Or native Linux / macOS

---

## 🧩 Project Structure

```text
project-root/
│
├── stack1/                 # Terraform: VPC, Aurora Serverless, S3, IAM
│   ├── main.tf
│   ├── outputs.tf
│   └── variables.tf
│
├── stack2/                 # Terraform: Bedrock Knowledge Base, IAM
│   ├── main.tf
│   ├── outputs.tf
│   └── variables.tf
│
├── modules/
│   ├── database/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── bedrock_kb/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── scripts/
│   ├── spec-sheets/        # Raw PDFs used for the KB
│   │   ├── bulldozer-bd850-spec-sheet.pdf
│   │   ├── dump-truck-dt1000-spec-sheet.pdf
│   │   ├── excavator-x950-spec-sheet.pdf
│   │   ├── forklift-fl250-spec-sheet.pdf
│   │   └── mobile-crane-mc750-spec-sheet.pdf
│   ├── aurora_sql.sql      # SQL to prep Aurora for vector storage
│   └── upload_s3.py        # Upload PDFs to S3
│
│
├── Screenshots/            # Evidence for rubric (Terraform, KB, DB, app)
│   └── ...png
│
├── app.py                  # Streamlit frontend (chat)
├── bedrock_utils.py        # Bedrock + KB integration & prompt validation
├── temperature_top_p_explanation.pdf
├── requirements.txt
├── .gitignore
└── README.md
````

---

## 🧑‍💻 Who Is This For?

This README assumes:

* You know **basic Python** and **Git**
* You have little/no production AWS experience
* You want **step-by-step guidance**: from setting up tools to running the final chat app

If you’re more advanced, you can skip to:

* [Quickstart](#-quickstart-if-youre-impatient)

---

## 📚 Learning Notes

This project helps you practice:

* **Building a full GenAI pipeline**:

  * Document ingestion → embedding → storage → retrieval → LLM response
* **Using AWS Bedrock** with Anthropic Claude 3 Haiku
* **Integrating Knowledge Bases** with Aurora Serverless
* **Using Terraform** for repeatable infra
* **Building a simple GenAI frontend** with Streamlit

---

## ✅ Prerequisites

### 1. Accounts & Permissions

You will need:

* An **AWS account** with:

  * Bedrock enabled in **`us-east-1`** (and access to **Anthropic Claude 3 Haiku** model ID
    `anthropic.claude-3-haiku-20240307-v1:0`)
  * Permissions to create:

    * VPC
    * Aurora Serverless PostgreSQL
    * S3 buckets
    * IAM roles & policies
    * Bedrock knowledge bases

> ⚠️ Some of these resources may incur cost. Clean up when you’re done (`terraform destroy`).

* A **GitHub account** (if you want to fork / push).

---

### 2. Local Machine: Tools to Install

You can do this entirely from **Linux/macOS**, or from **Windows via WSL2**.

#### If you’re on Windows (recommended: WSL2)

1. Install **WSL2** with Ubuntu:

   * Open **PowerShell as Administrator**:

     ```powershell
     wsl --install
     ```
   * Reboot if prompted.

2. Open **Ubuntu** from Start Menu.

3. Update packages:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

#### Tools (Linux, macOS, or WSL)

Install:

1. **Git**

   ```bash
   sudo apt install git -y
   ```

2. **Python 3.10+ & venv**

   ```bash
   python3 --version       # should be 3.10 or later
   sudo apt install python3-venv -y
   ```

3. **AWS CLI v2**
   Official guide: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

   Check version:

   ```bash
   aws --version
   # Example: aws-cli/2.31.x ...
   ```

4. **Terraform**
   Download from: [https://developer.hashicorp.com/terraform/downloads](https://developer.hashicorp.com/terraform/downloads)

   Or on Ubuntu:

   ```bash
   sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
   wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform -y
   terraform -version
   ```

5. **Python dependencies** will be installed later via:

   ```bash
   pip install -r requirements.txt
   ```

---

### 3. Configure AWS CLI

In WSL / terminal:

```bash
aws configure
```

Enter:

* AWS Access Key ID
* AWS Secret Access Key
* Default region: `us-east-1`
* Output format: `json` (or your preference)

Verify:

```bash
aws sts get-caller-identity
```

---

### 4. Confirm Bedrock and Model Access

List foundation models in `us-east-1`:

```bash
aws bedrock list-foundation-models --region us-east-1
```

Then confirm you see:

```text
"modelId": "anthropic.claude-3-haiku-20240307-v1:0"
```

Optionally, filter directly:

```bash
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query "modelSummaries[?modelId=='anthropic.claude-3-haiku-20240307-v1:0']"
```

---

### 5. Test Model Invocation via CLI (Optional but Helpful)

Create a file named `body.json`:

```json
{
  "anthropic_version": "bedrock-2023-05-31",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "Hello!" }
      ]
    }
  ],
  "max_tokens": 100
}
```

Then run:

```bash
aws bedrock-runtime invoke-model \
  --cli-binary-format raw-in-base64-out \
  --model-id anthropic.claude-3-haiku-20240307-v1:0 \
  --region us-east-1 \
  --content-type application/json \
  --accept application/json \
  --body file://body.json \
  response.json

cat response.json
```

You should see something like:

```json
{"role":"assistant","content":[{"type":"text","text":"Hello! How can I assist you today?"}]}
```

If this works, your Bedrock access is correctly configured.

---

## 🚀 Quickstart (If You’re Impatient)

For more experienced users:

```bash
# 1. Clone repo
git clone https://github.com/OnlyGhassan/aws-bedrock-project.git
cd aws-bedrock-project

# 2. Create & activate venv
python3 -m venv venv
source venv/bin/activate   # Windows WSL / Linux / macOS

# 3. Install deps
pip install -r requirements.txt

# 4. Deploy infra (stack1 then stack2)
cd stack1
terraform init
terraform apply    # note outputs
cd ../stack2
terraform init
terraform apply

# 5. Upload specs to S3
cd ..
python scripts/upload_s3.py

# 6. Run Streamlit app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🧱 Step-by-Step Setup (From Scratch)

### 1. Clone the Repository

From WSL/terminal:

```bash
cd /mnt/c/Users/<YourWindowsUser>/Downloads
git clone https://github.com/OnlyGhassan/aws-bedrock-project.git
cd aws-bedrock-project
```

> 💡 `/mnt/c/...` lets WSL access files on your Windows C: drive.

---

### 2. Create and Activate Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Deploy Infrastructure – Stack 1 (VPC, Aurora, S3, IAM)

1. Go into `stack1`:

   ```bash
   cd stack1
   ```

2. Initialize Terraform:

   ```bash
   terraform init
   ```

3. Review variables in `main.tf` / `variables.tf`:

   * AWS region (should be `us-east-1`)
   * VPC CIDR
   * Aurora configuration
   * S3 bucket name (e.g. `bedrock-kb-<your-unique-suffix>`)

4. Apply:

   ```bash
   terraform apply
   ```

   * Review the plan
   * Type `yes` to confirm

5. After it finishes, **copy the outputs** shown:

   * Aurora cluster endpoint
   * Database name / username
   * S3 bucket name
   * Secrets Manager secret name (RDS credentials)

You’ll need these for DB setup and stack2 configuration.

---

### 4. Configure Aurora PostgreSQL for Vector Storage

1. Go to **AWS Console → RDS → Query Editor v2**

2. Connect using the **secret** created by Terraform (RDS secret in Secrets Manager).

3. Open `scripts/aurora_sql.sql` from the repo and copy its content.

4. Run the script in the Query Editor to:

   * Enable necessary extensions (`pgvector` or related)
   * Create schema & tables (e.g., `bedrock_integration.bedrock_kb`)
   * Prepare DB for vector storage and Bedrock integration

5. Verify with:

   ```sql
   SELECT * FROM pg_extension;
   ```

   and:

   ```sql
   SELECT
       table_schema || '.' || table_name as show_tables
   FROM information_schema.tables
   WHERE table_type = 'BASE TABLE'
     AND table_schema = 'bedrock_integration';
   ```

These are also **required for the project rubric**.

---

### 5. Deploy Infrastructure – Stack 2 (Bedrock Knowledge Base)

1. Go into `stack2`:

   ```bash
   cd ../stack2
   ```

2. Initialize:

   ```bash
   terraform init
   ```

3. Update variables in `main.tf` / `variables.tf`:

   * Use the **S3 bucket** created by Stack 1
   * Point to the **Aurora cluster** and DB info
   * Ensure region is `us-east-1`

4. Apply:

   ```bash
   terraform apply
   ```

5. After apply:

   * Note the **Knowledge Base ID**
   * This is needed in the Streamlit app sidebar.

---

### 6. Upload PDF Spec Sheets to S3

The project includes sample PDFs in `scripts/spec-sheets/`.

The script `scripts/upload_s3.py` is configured to upload from a folder path into your S3 bucket.

Open `scripts/upload_s3.py` and Update:

* `folder_path` → match your local absolute path
* `bucket_name` → your bucket from Terraform outputs

Then run from project root:

```bash
cd ..
python scripts/upload_s3.py
```

You should see logs like:

```text
Successfully uploaded bulldozer-bd850-spec-sheet.pdf to <bucket>/spec-sheets/bulldozer-bd850-spec-sheet.pdf
...
```

---

### 7. Sync the Knowledge Base Data Source

1. Go to **AWS Console → Amazon Bedrock → Knowledge bases**
2. Open your Knowledge Base (from Terraform output)
3. Find its **data source** pointing to your S3 bucket
4. Click **Sync** (or equivalent) to ingest the documents
5. Wait until the sync shows **Success**

Now Bedrock KB has embeddings for your PDFs stored in Aurora.

---

## 💬 Running the Streamlit Chat Application

From the project root, with your virtual env active:

```bash
cd /mnt/c/Users/<YourWindowsUser>/Downloads/aws-bedrock-project
source venv/bin/activate
streamlit run app.py
```

You will see in the terminal:

```text
Local URL: http://localhost:8501
```

Open that in your browser (on Windows):
`http://localhost:8501`

### In the Streamlit app:

* **Sidebar**

  * Model: choose
    `anthropic.claude-3-haiku-20240307-v1:0`
  * Knowledge Base ID: paste the KB ID from Terraform/console
  * Temperature: default 0.2 (factual)
  * top_p: default 0.9 (reasonable variety)

* **Chat Input**

  * Ask questions like:

    * “What is the maximum load capacity of the excavator X950?”
    * “Which machine has the highest lifting capacity?”
    * “What is the fuel tank capacity of the forklift FL250?”

The app will:

1. Use **`valid_prompt`** to check if the question is:

   * Related to heavy machinery (allowed)
   * Or off-topic / disallowed (blocked)

2. Call **`query_knowledge_base`** to retrieve top relevant chunks

3. Call **`generate_response`** to send:

   * The context + your question
   * To Claude 3 Haiku on Bedrock

4. Show the answer in the chat, based only on your documents

---

## 🔍 Important Python Modules

### `bedrock_utils.py`

This file holds the main AWS logic.

#### 1. Bedrock Clients

```python
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

bedrock_kb = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1'
)
```

#### 2. `valid_prompt(prompt, model_id)`

* Uses Claude 3 Haiku to **classify** the user’s request into categories:

  * A: Model internals
  * B: Profanity/toxic
  * C: Unrelated
  * D: Asking how the model works
  * E: ONLY heavy machinery (allowed)
* Only if category **E** is returned does the app continue to answer.

#### 3. `query_knowledge_base(query, kb_id)`

* Calls `bedrock-agent-runtime.retrieve`:

  * `knowledgeBaseId=kb_id`
  * `retrievalQuery={"text": query}`
* Returns a list of:

  * `content` (text)
  * `source` (S3 URI)
  * `score` (relevance)

#### 4. `generate_response(prompt, model_id, kb_context, temperature, top_p)`

* Builds a final prompt like:

  > You are a helpful assistant specialized in heavy machinery.
  > Use ONLY this CONTEXT to answer.
  > CONTEXT: ...
  > QUESTION: ...

* Sends it to Claude 3 Haiku via `bedrock-runtime.invoke_model`

* Returns the assistant’s text answer

---

## 🌡 Temperature & `top_p` (Model Parameters)

The file `temperature_top_p_explanation.pdf` explains this in detail, but in short:

* **Temperature** controls how *random* or *creative* the model is:

  * Low (0–0.3): more deterministic, factual, stable
  * High (0.7–1.0): more creative, but can be less accurate
* **top_p** (nucleus sampling) controls how many possible tokens to consider:

  * Lower (e.g. 0.8): focus on most likely words
  * Higher (0.95–1.0): allow more variety

For this technical spec Q&A use case, we use:

* `temperature = 0.2` → more factual, consistent
* `top_p = 0.9` → some natural variety, but still controlled

You can adjust these from the **Streamlit sidebar**.


## 🛠 Troubleshooting

### 1. Terraform Errors

* **Provider / version issues**

  * Check your Terraform version:

    ```bash
    terraform -version
    ```
  * Ensure your AWS provider block is valid.

* **Permissions**

  * Make sure your IAM user/role can create:

    * VPC, RDS, S3, IAM roles, Bedrock KB

### 2. AWS Permissions / AccessDenied

If you see `AccessDeniedException` for Bedrock:

* Ensure you are using the correct AWS account (not an expired lab account)
* Make sure Bedrock is enabled in `us-east-1`
* Ensure your IAM permissions allow `bedrock:InvokeModel`, `bedrock:Retrieve`, etc.

### 3. `Invalid base64` When Calling Bedrock via CLI

If you see:

```text
Invalid base64: "{ ... }"
```

You **must** add:

```bash
--cli-binary-format raw-in-base64-out
```

to your `aws bedrock-runtime invoke-model` command.

### 4. WSL & Paths

* If `upload_s3.py` says the folder doesn’t exist:

  * Confirm the `folder_path` is correct and uses `/mnt/c/...`
* If Streamlit prints `gio: Operation not supported`:

  * Ignore it; just open `http://localhost:8501` manually in your Windows browser.

### 5. App Says “Your request cannot be processed…”

This means `valid_prompt` decided your question is **not category E** (not purely heavy machinery related).
Try asking a more on-topic question like:

* “What is the operating weight of the DT1000 dump truck?”

---

## 🧹 Clean Up

To avoid ongoing AWS charges:

1. Stop the Streamlit app and close your terminal.

2. In `stack2`:

   ```bash
   terraform destroy
   ```

3. In `stack1`:

   ```bash
   cd ../stack1
   terraform destroy
   ```

4. Confirm that:

   * VPC, RDS, S3 bucket, KB, IAM roles are deleted
   * No leftover high-cost resources exist

---

Feel free to fork this repo and adapt it to your own documents or domains (e.g., policies, internal docs, course materials).
