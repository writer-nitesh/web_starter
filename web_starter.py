import os
import sys
import http.server
from rich.console import Console

HandlerClass = http.server.SimpleHTTPRequestHandler
ServerClass = http.server.HTTPServer
console = Console()


def run_server():
    if len(sys.argv) > 2:
        project_name = sys.argv[2]
        index_html_path = os.path.join(project_name, "index.html")

        if not os.path.exists(index_html_path):
            console.print(
                "index.html' not found in the project directory.", style="bold red")
            return
        os.chdir(project_name)
        host()
    else:
        host()
    
def host():
    if "index.html" in os.listdir():
        server_address = ('localhost', 3000)
        httpd = ServerClass(server_address, HandlerClass)
        sa = httpd.socket.getsockname()
        console.print(
            f"Visit http://localhost:3000 or http://{sa[0]}:{sa[1]}")
        httpd.serve_forever()


def create_project(project_name, include_bootstrap=False):

    if os.path.exists(project_name):
        console.print(f"{project_name} already exists.", style="red")
        return

    # Create the project root directory
    project_root = project_name
    os.makedirs(project_root, exist_ok=True)

    # Create subdirectories
    subdirectories = ["styles", "scripts", "images", "fonts", "lib", "pages"]

    for subdir in subdirectories:
        os.makedirs(os.path.join(project_root, subdir), exist_ok=True)

    css_content = """* {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    .centered {
        text-align: center;
    }

    /* Your CSS code for outfit.css goes here */
    """

    # Create index.html
    index_html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{project_name}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="styles/outfit.css">
        {'''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'''
        if include_bootstrap else '''
        <link rel="stylesheet" type="text/css" href="styles/outfit.css">'''
        }
    </head>
    <body>
        {'''
        <div class="container h-100 d-flex justify-content-center align-items-center">
            <h1>Hello, World!</h1>
        </div>
        '''
        if include_bootstrap else '''
        <div class="centered">
            <h1>Hello, World!</h1>
        </div>
         '''
        }
    </body>
        {'''
        <script src="scripts/magic.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'''
        if include_bootstrap else '''
        <script src="scripts/magic.js"></script>'''
        }
    </html>
    """

    with open(os.path.join(project_root, "index.html"), "w") as f:
        f.write(index_html_content)

    # Create magic.js file in the scripts folder
    with open(os.path.join(project_root, "scripts", "magic.js"), "w") as f:
        f.write("// Your magic.js code goes here")

    # Create outfit.css file in the styles folder
    with open(os.path.join(project_root, "styles", "outfit.css"), "w") as f:
        f.write(css_content)

    console.print(f"Project created {project_name}", style="green")
    console.print(f"[blue]cd [white]{project_name}")
    console.print("use web_starter run to start the server")


def print_usage_guide():
    print("web_starter create_project <project_name> [-bootstrap]")
    print("web_starter run")
    print("web_starter help")


if __name__ == "__main__":
    if "run" in sys.argv:
        run_server()
    elif "create_project" in sys.argv:
        create_project(sys.argv[2], "-bootstrap" in sys.argv)
    elif "help" in sys.argv:
        print_usage_guide()
    else:
        console.print(
            "Usage: web_starter create_project <project_name> [-bootstrap]", style="yellow")
