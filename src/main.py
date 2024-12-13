import json, os, sys

sys.path.append('C:/Users/bhoja/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/site-packages')


from setup import Setup
Setup()

from markdown import markdown as md 
from pdfkit import *


wkhtml2pdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

mainDir = os.path.dirname(os.path.abspath(__file__))
assetdDir = os.path.join(mainDir, 'assets')
imagesDir = os.path.join(mainDir, 'imgs')

CV_data_file_path = os.path.join(mainDir, 'data.jsonc')
default_output_file_name = "sample"

class ResumeBot:
    def __init__(self, data_file_path: os.path, output_file_path: os.path) -> None:
        self.data_file_path = data_file_path
        self.output_file_path = output_file_path

        self.data = self.get_json_data()
        self.format = self.get_json_data(os.path.join(assetdDir, 'format.jsonc'))
        self.styles = self.get_json_data(os.path.join(assetdDir, 'styles.jsonc'))

        self.images = os.listdir(imagesDir)

        self.badge = self.get_json_data(os.path.join(assetdDir, 'badge.jsonc'))
        self.default_icon = "https://img.shields.io/badge/$KEY-%23000000.svg?style=plastic&logoColor=white"
        icons_set1 = {j: k for _, i in self.badge["Tech Stack"].items() for j, k in i.items()}
        icons_set2 = self.badge["Socials"]
        self.icons = {**icons_set1, **icons_set2}

    def get_json_data(self, json_file_path: os.path = None) -> dict:
        active_file_path = json_file_path if json_file_path else self.data_file_path

        with open(active_file_path) as f:
            if 'jsonc' in active_file_path:
                y = [i.strip() for i in f.readlines() if i.strip() != '']
                y = [i for i in y if not i.startswith('// ')]
                y_str = '\n'.join(y)

            else:
                y_str = f.read()

        return json.loads(y_str)
    
    def get_active_data(self, data: dict) -> dict|None:
        ret = {}

        def check(data: dict|list) -> dict|list|None:
            if type(data) == dict:
                x = {}

                for k, v in data.items():
                    if (v != None) and (v != "") and (v != []) and (v != {}):
                        x[k] = check(v)

                return x

            if type(data) == list:
                return [check(i) for i in data if (i != None) and (i != "") and (i != []) and (i != {})]

            return data

        for k, v in data.items():
            if (v != None) and (v != "") and (v != []) and (v != {}):
                ret[k] = check(v)

        return ret if ret else None

    def organiser(self, data: dict) -> str:
        ret = ''

        for k, v in data.items():
            if k == '$STYLE':
                self.icons = {u: w.replace('$STYLE', v['Icon']) for u, w in self.icons.items()}

            if k.lower() == 'name':
                ret += f'{self.format["h1"]} {v}\n\n'

            if k.lower() == "contacts":
                a = ""

                for i, j in v.items():
                    DI = self.default_icon
                    try:
                        icon_url = self.icons[i]

                    except KeyError:
                        icon_url = DI.replace('$KEY', i)

                    a += self.format["button"].replace("$", i).replace("&", icon_url).replace("@", j) + '\n'

                ret += a + '\n'

            if k.lower() == "summary":
                ret += f'{self.format["h2"]} {k.capitalize()}\n{v}\n\n'

            if k.lower() == "education":
                a = f"{self.format['h2']} {k.capitalize()}\n"

                for r in v:
                    x = ""

                    for i, j in r.items():
                        if i.lower() == 'institute':
                            x += f"{self.format['h3']} {j}"

                        if i.lower() == "duration":
                            x += f' ({self.format["italic"].replace("$", j)})\n'

                        if i.lower() == "degree":
                            x += f'{self.format["bullet"]} {self.format["bold"].replace("$", "Cource")}: {j}\n'

                        if i.lower() == "cgpa":
                            x += f'{self.format["bullet"]} {self.format["bold"].replace("$", "CGPA")}: {j}\n'

                        if i.lower() == "sgpa":
                            x += f'{self.format["bullet"]} {self.format["bold"].replace("$", "SGPA")}: {j}\n'

                    a += x+"\n"

                ret += a

            if k.lower() == "experience":
                pass

            if k.lower() == "achievements":
                pass

            if k.lower() == "skills":
                a = f"{self.format['h2']} {k.capitalize()}\n"

                for k, v in v.items():
                    b = f"{self.format['h3']} {k}\n"

                    for z in v:
                        DI = self.default_icon
                        try:
                            icon_url = self.icons[z]

                        except KeyError:
                            icon_url = DI.replace('$KEY', z)

                        b += self.format["label"].replace("$", z).replace("@", icon_url) + '\n'

                    a += f'{b}\n'

                ret += a

            if k.lower() == "projects":
                a = f"{self.format['h2']} {k.capitalize()}\n"

                for r in v:
                    x = ""

                    for i, j in r.items():
                        if i.lower() == 'name':
                            x += f"{self.format['h3']} {j}\n"

                        if i.lower() == "role":
                            x += f'{self.format["bullet"]} {self.format["bold"].replace("$", "My Role")}: {", ".join([self.format["italic"].replace("$", p) for p in j])}\n'

                        if i.lower() == "description":
                            x += f'{self.format["bullet"]} {self.format["bold"].replace("$", "Description")}: {j}\n'

                    a += x+"\n"

                ret += a

            if k.lower() == "connections":
                a = f"{self.format['h2']} Memberships and Position\n"

                for p in v:
                    a += f'{self.format["bullet"]} {self.format["bold"].replace("$", p["org"])} ({self.format["italic"].replace("$", p["duration"])}): {p["position"]}\n'

                ret += a

        return ret

    def mk_markdown(self, stripped_data: str, opt_file: os.path) -> str:
        if not os.path.exists(opt_file):
            _ = open(opt_file, "w").close()

        with open(opt_file, "w") as f:
            f.write(stripped_data)

    def md2pdf(self, wkHTMLtoPDF_path: os.path, markdown_data: str, opt_file: os.path = None, border_in_inch: int = 1, paper_size: str = "A4", orientation: str = "Portrait", encoding: str = "UTF-8") -> str:
        pdf_file_path = opt_file if opt_file else self.output_file_path
        cfg = configuration(wkhtmltopdf=wkHTMLtoPDF_path)
        html_text = md(markdown_data).replace("&amp;", "&")

        options = {
            'page-size': paper_size,
            'margin-top': f'{border_in_inch}in',
            'margin-right': f'{border_in_inch}in',
            'margin-bottom': f'{border_in_inch}in',
            'margin-left': f'{border_in_inch}in',
            'encoding': encoding,
            'custom-header': [('Accept-Encoding', 'gzip')],
            'no-outline': None,
            'orientation': orientation,
            'user-style-sheet': f'data:text/css;charset={encoding};base64,'
                                'Lm1vbm9zcGFjZSB7IGZvbnQtZmFtaWx5OiBtb25vc3BhY2U7IH0='
        }

        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)

        try:
            from_string(html_text, opt_file, configuration=cfg, options=options)

        except Exception as e:
            print(e)


def main():
    md_opt_file_path = os.path.join(mainDir, f'{default_output_file_name.upper()}.md')
    pdf_opt_file_path = os.path.join(mainDir, f'{default_output_file_name}.pdf')

    RB = ResumeBot(CV_data_file_path, md_opt_file_path)

    active_data = RB.get_active_data(RB.data)
    md_datta = RB.organiser(active_data)

    RB.md2pdf(wkhtml2pdf_path, md_datta, pdf_opt_file_path)
    print(f"\033[1;32m[+] DynamicCVGeneratorMessage: \033[0mPDF successfully at '\033[1m{pdf_opt_file_path}\033[0m'.")

    x = input(f"\033[1;33m[+] DynamicCVGeneratorNotification: \033[0mDo you want to keep the markdown file? [y/N]: ").lower()

    if x.startswith("y"):
        xp = input(f"\033[1m>>> \033[0mWhere to keep the markdown file? ")
        if xp == "": xp = md_opt_file_path
        RB.mk_markdown(md_datta, xp)
        print(f"\033[1;32m[+] DynamicCVGeneratorMessage: \033[0mMarkdown successfully at '\033[1m{xp}\033[0m'.")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n\033[1;91m[!] DynamicCVGeneratorMessage: \033[0mProgram terminated by user.\033[0m")
        exit(1)
