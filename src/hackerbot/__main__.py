import sys
from .mcp_api import start_mcp_server


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python -m hackerbot [mcp]")
        print("Commands:")
        print("  mcp         Start the MCP server (fastmcp required)")
        sys.exit(0)

    command = sys.argv[1]
    if command == "mcp":
        # Optionally parse host/port from sys.argv
        host = "0.0.0.0"
        port = 8000
        if len(sys.argv) > 2:
            host = sys.argv[2]
        if len(sys.argv) > 3:
            port = int(sys.argv[3])
        print(f"Starting MCP server on {host}:{port} ...")
        start_mcp_server(host=host, port=port)
    else:
        print(f"Unknown command: {command}")
        print("Use -h or --help for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
