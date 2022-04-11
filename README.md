## Hosts_Scan

Hosts_Scan是一款Host碰撞工具，在使用Host碰撞过程中针对一些问题进行改进，增加如下功能

- 域名有效性验证
- Title黑名单
- 获取Title失败时，只记录返回长度300以上结果

具体实践参考：[深夜火器内测群群聊小记之HOST碰撞](https://zone.huoxian.cn/d/145-host)

### 使用

```
python3 hosts_scan.py -d domain.txt -s subdomain.txt -i ip.txt
```

#### 参数
```
-i    IP file
-s    Subdomain file
-d    Domain file
-T    Threads，Default 20
```

### Todo

目前针对C段进行碰撞时，会出现大量脏数据，后续计划进行如下优化

- 单一IP出现大量结果返回长度一致时，进行丢弃
- 扫描前获取每个IP初始Title，加入黑名单

### Thanks

https://github.com/fofapro/Hosts_scan