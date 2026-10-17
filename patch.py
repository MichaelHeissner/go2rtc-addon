import re

p = "pkg/mdns/client.go"
s = open(p).read()

s, n1 = re.subn(r"return !xnet\.Docker\.Contains\(ip\)", "return mdnsAllowed(ip)", s)
assert n1 == 1, "filter line not found"

s, n2 = re.subn(
    r"(\t+)(_ = SetsockoptIPMreq\(fd, syscall\.IPPROTO_IP, syscall\.IP_ADD_MEMBERSHIP, mreq\))(\s*)for _, send := range b\.Sends",
    lambda m: m.group(1) + "if !mdnsRestricted() {\n" + m.group(1) + "\t" + m.group(2) + "\n" + m.group(1) + "}" + m.group(3) + "for _, send := range b.Sends",
    s,
)
assert n2 == 1, "default membership line not found"
open(p, "w").write(s)

open("pkg/mdns/restrict.go", "w").write('''package mdns

import (
	"bufio"
	"net"
	"os"
	"strings"

	"github.com/AlexxIT/go2rtc/pkg/xnet"
)

// Networks from env GO2RTC_MDNS_NETS (comma separated CIDR) or from the file
// /config/go2rtc-mdns.txt (one CIDR per line). If none are set: original behavior.
var allowedNets = loadAllowedNets()

func loadAllowedNets() []*net.IPNet {
	var list []string
	if v := os.Getenv("GO2RTC_MDNS_NETS"); v != "" {
		list = strings.FieldsFunc(v, func(r rune) bool { return r == ',' || r == ' ' })
	} else if f, err := os.Open("/config/go2rtc-mdns.txt"); err == nil {
		defer f.Close()
		sc := bufio.NewScanner(f)
		for sc.Scan() {
			line := strings.TrimSpace(sc.Text())
			if line != "" && !strings.HasPrefix(line, "#") {
				list = append(list, line)
			}
		}
	}
	var nets []*net.IPNet
	for _, s := range list {
		if _, n, err := net.ParseCIDR(s); err == nil {
			nets = append(nets, n)
		}
	}
	return nets
}

func mdnsRestricted() bool {
	return len(allowedNets) > 0
}

func mdnsAllowed(ip net.IP) bool {
	if !mdnsRestricted() {
		return !xnet.Docker.Contains(ip)
	}
	for _, n := range allowedNets {
		if n.Contains(ip) {
			return true
		}
	}
	return false
}
''')
print("patched")
