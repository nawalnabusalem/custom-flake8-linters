# NWL100: Assert without message
def test_assert_no_message():
    x = 5
    assert x == 5  # Error: Assert statement missing message


# NWL101: Poorly formatted function call
def poorly_formatted_call():
    connect('localhost', 8080, 20,
          True)  # Error: Bad function call formatting


# NWL102: Keyword arguments formatting
def keyword_args_issue():
    connect(host='localhost',
            port=8080, timeout=30,
            debug=True)  # Error: Keyword arguments not properly formatted


# NWL103: Missing empty line after control statement
if True:
    print("No empty line after control statement")  # Error
print("This should have a blank line above")


# NWL104: Missing empty line before control statement
def func():
    x = 1
    if x > 0:  # Error: No blank line before control statement
        pass


# Correct Examples (Should Pass All Checks)
def good_examples():
    # NWL100: Assert with message
    assert 1 == 1, "Optional message here"

    # NWL101: Well-formatted call
    print(
        "Properly formatted",
        "function call"
    )

    # NWL102: Proper keyword args
    connect(
        host='localhost',
        port=8080,
        timeout=30
    )

    # NWL103/104: Proper spacing
    value = 10

    if value > 5:
        print("Correct spacing")

    print("End")
