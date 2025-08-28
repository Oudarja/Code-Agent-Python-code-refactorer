import textwrap
from services.code_diff_service import generate_code_diff
from loguru import logger
def test_basic_diff():
    old_code = """def greet(name):
    print(f"Hello, {name}!")"""

    new_code = """def greet(name: str) -> None:
    print(f"Hello, {name}!")"""

    expected_diff = textwrap.dedent("""\
       --- Original
+++ Refactored
@@ -1,2 +1,2 @@
-def greet(name):
+def greet(name: str) -> None:
     print(f"Hello, {name}!")
    """)

    actual_diff = generate_code_diff(old_code, new_code)
    logger.info(actual_diff)

    assert actual_diff.strip() == expected_diff.strip()
