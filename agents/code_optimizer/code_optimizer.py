from redbaron import RedBaron
from collections import defaultdict


class CodeOptimizer:
    def __init__(self, code: str):
        self.code = code

    def optimize_imports(self):
        red = RedBaron(self.code)
        imports = red.find_all('ImportNode')
        from_imports = red.find_all('FromImportNode')

        import_dict = defaultdict(list)

        all_imports = []

        for import_node in from_imports:
            from_module = '.'.join(import_node.full_path_names()[0].split('.')[:-1])
            imported_modules = [node.split('.')[-1]for node in import_node.full_path_names()]
            import_dict[from_module].extend(imported_modules)
            import_dict[from_module] = list(set(import_dict[from_module]))

        for key in import_dict.keys():
            all_imports.append(f"from {key} import {', '.join(import_dict[key])}")

        for import_node in imports:
            if import_node.dumps().strip() not in all_imports:
                all_imports.append(import_node.dumps())

        all_imports = sorted(all_imports, key=len)
        all_imports = '\n'.join(all_imports)

        return all_imports.strip()

    def optimize_classes(self):
        red = RedBaron(self.code)
        extracted_classes = []

        for node in red:
            if node.type == "class":
                extracted_classes.append(node.dumps().strip())

        extracted_code = "\n\n\n".join(extracted_classes)

        return extracted_code.strip()

    def optimize_functions(self):
        red = RedBaron(self.code)
        extracted_functions = []

        for node in red:
            if node.type == "def":
                extracted_functions.append(node.dumps().strip())

        extracted_code = "\n\n\n".join(extracted_functions)

        return extracted_code.strip()
