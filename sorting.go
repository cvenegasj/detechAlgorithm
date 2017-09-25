package main

import (
	"strconv"
	"strings"
)

type ByDetechTag []string

func (s ByDetechTag) Len() int {
	return len(s)
}

func (s ByDetechTag) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}
func (s ByDetechTag) Less(i, j int) bool {
	if strings.Contains(s[i], "detech") && strings.Contains(s[j], "detech") {
		n1, err := strconv.Atoi(strings.Replace(strings.Split(s[i], "_")[0], "img", "", -1))
		if err != nil {
			panic(err)
		}
		n2, err := strconv.Atoi(strings.Replace(strings.Split(s[j], "_")[0], "img", "", -1))
		if err != nil {
			panic(err)
		}
		return n1 < n2
	}else {
		return false
	}


}
