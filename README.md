# custom-flake8-linters
This project implements several custom Flake8 linters, each targeting a specific code style or quality rule. Below is a detailed explanation of each linter:


**🛠️ NWL100: CheckAssertMessageLinter (AssertMessageChecker)**
- **Purpose:** Ensures that all assert statements include a descriptive message. 
- **Why:** Adding a message to assertions helps clarify the reason for the assertion failure, making debugging easier.
  
**Example:**
  ```bash
  # ❌ Incorrect:
  assert x == 5
  
  # ✅ Correct:
  assert x == 5, "x should be equal to 5"
  ```


**🛠️ NWL102: CheckKeywordsFunctionCallLinter (KeywordsFunctionCallChecker)**
- **Purpose:**  Checks that function calls **use keyword arguments instead of positional arguments** to improve clarity and reduce errors.
It enforces that calls must explicitly name their arguments unless the function is a built-in allowed to be called positionally.
  
- **Why:** Using keyword arguments makes the code more readable and less error-prone by clearly associating values with parameter names.
Some built-in functions are allowed to be called positionally, and these can be whitelisted in a BUILTIN_FUNCTIONS list to skip the check.

- **How to configure:** Add any built-in functions that should be exempted from this rule to the `BUILTIN_FUNCTIONS` list inside `linters/CheckKeywordsFunctionCallLinter.py`.
  
**Example:**
  ```bash
# ❌ Incorrect - positional argument used:
my_func(1, 2)

# ✅ Correct - keyword arguments used:
my_func(a=1, b=2)

# ✅ Allowed - positional call to a whitelisted built-in function:
print("Hello, world!")

  ```
**🛠️  NWL103: CheckEmptyLineAfterStatementLinter (EmptyLineAfterStatementChecker)**
- **Purpose:**  Ensures there is **an empty line after specific code blocks or statements** such as function definitions, control structures, and flow statements.
  
- **Why:** Visually separating logic blocks helps with readability and reduces cognitive load when scanning code.

- **What it checks:** This linter requires an empty line after the following statements:
    - `def` and `class` definitions.
    - Control structures: `if`, `for`, `while`, `try`, `with`, and their clauses (`else`, `except`, `finally`).
    - Flow-related statements: `return`, `break`, `continue`, `raise`, `assert`.
      
**Example:**
  ```bash
# ❌ Incorrect:
def example():
    if condition:
        do_something() # ← no empty line after if body
    else:
        handle()
    log()  # ← no empty line after else clause

# ✅ Correct
def example():
    if condition:
        do_something()

    else:
        handle()

    log()

  ```

**🛠️   NWL104: CheckEmptyLineBeforeStatementLinter (EmptyLineBeforeStatementChecker)**
- **Purpose:**  Ensures there is an **empty line before certain statements**, such as control blocks and function/class definitions — unless they are **the first child** of their parent node. 
  
- **Why:** Enhances code readability and logical separation. Skipping inline comments ensures developers can keep meaningful notes without affecting linter behavior.
  
- **Key Features:** This linter requires an empty line after the following statements:
    - Skips comment lines when checking for the first empty line.
    - Supports spacing before:
        - `def`, `class`.
        - `if`, `else`, `elif`.
        - `try`, `except`, `finally`.
        - `return`, `raise`, `assert`.
    - Does not trigger if the statement is the first child (e.g. first line inside a function/class).
 
**Example:**
  ```bash
# ❌ Incorrect
def func():
    prepare()
    if condition:
        do_stuff()

# ✅ Correct
def func():
    prepare()

    if condition:
        do_stuff()

  ```

  ```bash
# ❌ Incorrect (comment line does not count as spacing)
def func():
    process()
    # this handles the fallback
    else:
        fallback()

# ✅ Correct
def func():
    process()

    # this handles the fallback
    else:
        fallback()

  ```
# ⚙️ How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run `flake8` with Your Linters**
From your project or any Python codebase you want to lint:
   ```bash
   flake8 path/to/your/code
   ```
  You should now see violations reported using your custom rule codes:
   ```bash
  ./Flake8Examples.py:4:5: NWL100 Empty assert message detected. Provide a descriptive message.
  ./Flake8Examples.py:9:5: NWL102 Non builtin positional function call detected. Pass the call with keyword arguments
  ./Flake8Examples.py:22:51: NWL103 required an empty line after if body
  ./Flake8Examples.py:29:5: NWL104 required an empty line before If statement
   ```

# 🧪 Continuous Integration (CI)
This project uses **GitHub Actions** to automatically run Flake8 code style checks on every `push` and `pull request`.
1. **🔄 Workflow:** `Code Style Linters CI` 

- **Triggers:** Runs on every push and pull request.
- **Python Setup:** Uses Python 3.12.
- **Caching:** Caches pip packages to speed up installs.
- **Linting:** Runs flake8 and stores the results in a log file.
- **Artifacts:** Uploads the flake8_logs_results.txt for reference.
- **Notifications:** Automatically sends an email with the linting results using dawidd6/action-send-mail.

2. **💌 Email includes:**

- Job status (success/failure).
- The exact flake8 logs.
- Commit and repository info.
![image](https://github.com/user-attachments/assets/2aa4652a-a65b-4ef3-8819-7b7ad1c77bcb)


