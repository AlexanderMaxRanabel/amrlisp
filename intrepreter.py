def lisp_eval(ast, env):
    if isinstance(ast, str):
        if ast.startswith("'"):
            return ast[1:]
        else:
            return env[ast]
    elif isinstance(ast, list):
        if ast[0] == "quote":
            (_, exp) = ast
            return exp
        elif ast[0] == "if":
            (_, test, conseq, alt) = ast
            exp = (conseq if lisp_eval(test, env) else alt)
            return lisp_eval(exp, env)
        elif ast[0] == "define":
            (_, var, exp) = ast
            env[var] = lisp_eval(exp, env)
        elif ast[0] == "lambda":
            (_, params, body) = ast
            return (params, body, env)
        else:
            proc = lisp_eval(ast[0], env)
            args = [lisp_eval(arg, env) for arg in ast[1:]]
            if callable(proc):
                return proc(*args)
            else:
                params, body, env_ = proc
                new_env = {}
                new_env.update(env_)
                new_env.update(zip(params, args))
                return lisp_eval(body, new_env)
    else:
        return ast

def lisp_print(exp):
    if isinstance(exp, str):
        return exp
    elif isinstance(exp, list):
        return "(" + " ".join(map(lisp_print, exp)) + ")"
    else:
        return str(exp)

def lisp_repl():
    env = {}
    while True:
        line = input("lisp>>> ")
        if line.strip() == "":
            continue
        exp = lisp_parse(line)
        val = lisp_eval(exp, env)
        print(lisp_print(val))

def lisp_parse(s):
    i, l = 0, len(s)
    def skip_spaces():
        nonlocal i
        while i < l and s[i].isspace():
            i += 1
    def parse_exp():
        nonlocal i
        skip_spaces()
        if i == l:
            raise Exception("unexpected EOF while reading")
        c = s[i]
        i += 1
        if c == "(":
            result = []
            skip_spaces()
            while s[i] != ")":
                result.append(parse_exp())
                skip_spaces()
            i += 1
            return result
        elif c == "'":
            return ["quote", parse_exp()]
        elif c.isdigit() or c == "-":
            j = i
            while i < l and s[i].isdigit():
                i += 1
            return int(s[j-1:i])
        else:
            j = i
            while i < l and not s[i].isspace() and s[i] != "(" and s[i] != ")":
                i += 1
            return s[j-1:i]
    return parse_exp()

lisp_repl()

