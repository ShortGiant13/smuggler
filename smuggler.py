import requests

def check_smuggling(url, headers):
    # Send the request and get the response
    response = requests.post(url, headers=headers)

    # Check for HTTP smuggling
    if "Transfer-Encoding" in response.headers and "Content-Length" in response.headers:
        print("[+] Possible HTTP smuggling detected!")
        return True
    elif "Transfer-Encoding" in response.headers and "Content-Length" not in response.headers:
        print("[+] HTTP smuggling (TE.CL) detected!")
        return True
    elif "Content-Length" in response.headers and "Transfer-Encoding" not in response.headers:
        print("[+] HTTP smuggling (CL.TE) detected!")
        return True
    elif "Content-Type" in response.headers and "Transfer-Encoding" in response.headers and "Content-Length" in response.headers:
        if "boundary" in response.headers["Content-Type"]:
            print("[+] HTTP smuggling (mime) detected!")
            return True
        elif "chunked" in response.headers["Transfer-Encoding"] and "gzip" in response.headers["Content-Encoding"]:
            print("[+] HTTP smuggling (chunked+gzip) detected!")
            return True
        else:
            return False
    else:
        return False

def check_all_urls(urls, headers):
    # Loop through all URLs and check for HTTP smuggling
    for url in urls:
        print("[*] Checking URL:", url)
        if check_smuggling(url, headers):
            print("[*] The URL", url, "is vulnerable to HTTP smuggling!")
        else:
            print("[*] The URL", url, "is not vulnerable to HTTP smuggling.")

if __name__ == "__main__":
    # Get the target URLs from the user
    urls = []
    while True:
        url = input("[?] Enter a URL to test for HTTP smuggling (or 'done' to finish): ")
        if url.lower() == "done":
            break
        urls.append(url)

    # Get the headers to be sent in the request from the user
    headers = {}
    while True:
        header_name = input("[?] Enter a header name (or 'done' to finish): ")
        if header_name.lower() == "done":
            break
        header_value = input("[?] Enter the value for header '" + header_name + "': ")
        headers[header_name] = header_value

    check_all_urls(urls, headers)