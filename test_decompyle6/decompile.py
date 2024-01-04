import os
import uncompyle6

def decompile_so_file(so_file, output_file):
    print(so_file)
    print(output_file)
    with open(so_file, "rb") as fin:
        so_content = fin.read()

    py_code = uncompyle6.decompile_file(so_content)

    with open(output_file, "w") as fout:
        fout.write(py_code)


if __name__=="__main__":
    so_files = [f for f in os.listdir("./") if f[-3:]=="pyc"]
    for so_file in so_files:
        output_file = so_file+".py"
        print(f"{so_file} -> {output_file}")
        decompile_so_file(so_file, output_file)
