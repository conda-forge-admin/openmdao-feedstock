import os
import subprocess
import sys
from os.path import join, dirname

import openmdao

# don't test the code_review stuff
TESTFLO = """[testflo]
skip_dirs =
  code_review
"""


def main() -> int:
    with open(".testflo", "w") as fp:
        fp.write(TESTFLO)

    test_files_to_delete = [
        # can't test these, yet, because of playwright
        ["visualization", "n2_viewer", "tests", "test_gui.py"],
        ["docs", "openmdao_book", "tests", "test_jupyter_gui_test.py"],
        # https://github.com/conda-forge/openmdao-feedstock/pull/74
        #  File ".../tests/test_functional_interface.py", line 376
        #  assert_near_equal(J2[*jac_index_map['circle.area', 'x']], darea_dx_expected, tolerance=1e-12)
        #                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #  SyntaxError: invalid syntax. Perhaps you forgot a comma?
        ["core", "tests", "test_functional_interface.py"],
    ]

    for tf2d in test_files_to_delete:
        os.unlink(join(dirname(openmdao.__file__), *tf2d))

    return subprocess.call(
        [
            "testflo",
            "--config",
            ".testflo",
            "--stop",
            "-v",
            "--pre_announce",
            "--numprocs",
            os.environ["CPU_COUNT"],
            "openmdao",
            "--exclude",
            "*test_simple_paraboloid_desvar_indices_COBYQA*",
        ]
    )


if __name__ == "__main__":
    sys.exit(main())
