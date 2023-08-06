from TheSilent.clear import clear
from TheSilent.sql_injection_scanner import sql_injection_scanner
from TheSilent.xss_scanner import xss_scanner

CYAN = "\033[1;36m"

# scans for security flaws and bad practices
def web_scanner(url, secure=True, tor=False, delay=1, report=True):
    clear()

    my_sql_injection_scanner = sql_injection_scanner(url=url, secure=secure, tor=tor, delay=delay)
    my_xss_scanner = xss_scanner(url=url, secure=secure, tor=tor, delay=delay)

    clear()

    print(CYAN + "sql injection:")

    for i in my_sql_injection_scanner:
        if report:
            with open(url +  ".txt", "a") as f:
                f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "xss:")

    for i in my_xss_scanner:
        if report:
            with open(url +  ".txt", "a") as f:
                f.write(i + "\n")
                
        print(CYAN + i)
