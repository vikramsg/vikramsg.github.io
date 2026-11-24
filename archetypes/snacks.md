---
title: "{{ replace (substr .File.ContentBaseName 11) "-" " " | title }}"
date: {{ .Date | time.Format "2006-01-02" }}
---
