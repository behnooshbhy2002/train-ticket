import os
import subprocess
from openai import OpenAI

# Initialize the Novita AI client
client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key="6e03f062-926f-4d3e-ac1a-c07729d5b947",
)

# Model configuration
model = "meta-llama/llama-3.1-8b-instruct"
stream = False
max_tokens = 1024

# Paths for files
TEST_FILE_F = "app\\features\\ticket_verification.feature"  # Path to your test file
TEST_FILE_C = "app\\features\\steps\\verify_ticket_steps.py"  # Path to your step definitions
LOG_FILE = "find_fix_error_automatic\\error_log.txt"  # File to store combined test output and errors
UPDATED_CODE_FILE = "find_fix_error_automatic\\updated_code.py"  # File to save the updated code
LLM_RESPONSE_FILE = "find_fix_error_automatic\\llm_response.txt"  # File to save the full LLM response

# Step 1: Run the test and write output in the desired format
def run_test():
    print("Running tests...")
    all_tests_passed = False  # Flag to track test results

    with open(LOG_FILE, "w") as log_file:
        # Run the behave test and capture the output
        process = subprocess.run(
            ["behave", TEST_FILE_F],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        test_output = process.stdout

        # Write the test code to the log file
        log_file.write("In my test:\n")
        log_file.write("# Test code\n")
        with open(TEST_FILE_C, "r") as test_file:
            log_file.write(test_file.read())
        
        # Check if the test passed or failed
        if "0 failed" in test_output:
            log_file.write("\nEverything is OK. Test passed successfully.\n")
            print("Everything is OK. Test passed successfully.")
            all_tests_passed = True  # Set the flag to True
        else:
            log_file.write("\nI have this error:\n")
            log_file.write("# Error message\n")
            log_file.write(test_output)
            print("Errors found. Combined log saved to", LOG_FILE)

    return all_tests_passed  # Return the flag to indicate test results


# Step 2: Send the test results to the LLM and request updated code
def get_updated_code():
    print("Sending test results to LLM for analysis...")
    with open(LOG_FILE, "r") as log_file:
        test_results = log_file.read()

    # Prompt to send to the LLM
    prompt = f"""
I ran the following test for a ticket verification system, and these are the results:

{test_results}

Based on the errors in the test results, please provide an updated version of the code that fixes the issues. 
Make sure the code is complete and ready to replace the existing implementation. just write code to explaination.
"""

    # Call the Novita AI API
    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=stream,
        max_tokens=max_tokens,
    )

    # Extract the full response
    llm_response = chat_completion_res.choices[0].message.content

    # Save the full response to a file
    with open(LLM_RESPONSE_FILE, "w") as response_file:
        response_file.write(llm_response)
    print(f"LLM response saved to {LLM_RESPONSE_FILE}")

    # Extract the code portion (enclosed in ``` #code ```)
    start_marker = "```python"
    end_marker = "```"

    if start_marker in llm_response and end_marker in llm_response:
        start_index = llm_response.index(start_marker) + len(start_marker)
        end_index = llm_response.index(end_marker, start_index)
        updated_code = llm_response[start_index:end_index].strip()
    else:
        updated_code = "# No code provided in LLM response"

    # Save the extracted code to a file
    with open(UPDATED_CODE_FILE, "w") as code_file:
        code_file.write(updated_code)

    print(f"Updated code saved to {UPDATED_CODE_FILE}")


# Main workflow
if __name__ == "__main__":
    all_tests_passed = run_test()  # Step 1: Run the initial test

    if all_tests_passed:
        # If all tests pass, log a success message and skip the API call
        print("All tests passed successfully. No need to call the LLM.")
    else:
        # If tests fail, proceed to call the LLM and get updated code
        get_updated_code()  # Step 2: Send results to LLM and get updated code
