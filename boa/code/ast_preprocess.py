from bytecode import Bytecode
import ast
from ast import NodeTransformer, NodeVisitor
import inspect
import pdb
import dis


class RewriteDicts(NodeTransformer):

    last_store_name = None

    updated_dicts = []

    def visit_Dict(self, node):
        if len(node.keys):

            if self.last_store_name and self.last_store_name.id and self.last_store_name.lineno == node.lineno:
                for item in node.values:
                    if isinstance(item, ast.Dict):
                        raise Exception("Cannot use dictionaries inside of dictionaries")

                node.name = self.last_store_name.id
                self.updated_dicts.append(node)
                self.last_store_name = None
            else:
                raise Exception("Dictionary names must be declared")

        return ast.Dict(keys=[], values=[], lineno=node.lineno)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.last_store_name = node
        else:
            self.last_store_name = None
        return node


def preprocess_method_body(source_code_obj):

    src = inspect.getsource(source_code_obj)

    ast_tree = ast.parse(src)

    visitor = RewriteDicts()
    ast_tree = visitor.visit(ast_tree)

    ast.fix_missing_locations(ast_tree)
    updated_code = compile(ast_tree, filename='<ast>', mode='exec')
    bc = Bytecode.from_code(updated_code)

    dlist = visitor.updated_dicts
    RewriteDicts.updated_dicts = []
    RewriteDicts.last_store_name = None

    return bc[0].arg, dlist
