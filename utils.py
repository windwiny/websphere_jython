# encoding: UTF-8
import sys, os
import time
import re

print __name__, 'load', time.strftime("%Y%m%d%H%M%S")

def create_all_help():
    for na in globals().keys():
        if not na.startswith('Admin'):
            continue
        m = eval(na)
        txt = m.help()
        print 'Create %s   %s' % (na, len(txt))
        f = open('%s.txt' % na, 'w')
        f.write(txt)
        f.close()

def create_attributes(fn=r"_attributes.txt"):
    f = open(fn, 'wb')
    for na in AdminConfig.types().splitlines():
        if na.startswith('com.') or na.startswith('org.'):
            continue
        print 'Get  %s  attributes' % na
        f.write( "# %s\r\n" % na)
        f.flush()
        f.write(AdminConfig.attributes(na))
        f.write("\r\n\r\n\r\n")
    f.close()

def get_all_info(fn='', skip=''):
    if not fn:
        fn = 'all_info_%s_%s.txt' % (AdminControl.getCell(), time.strftime("%Y%m%d%H%M%S"))
        print "info file name %s\n" % fn
    if skip:
        ff = 'ab'
    else:
        ff = 'wb'
    f = open(fn, ff)

    for na in AdminConfig.types().splitlines():
        if na.startswith('com.') or na.startswith('org.'):
            continue
        if skip and na <= skip:
            print 'skip %s' % na
            continue
        if na in ['DisplayName', 'J2EEEObject']:
            print '%s  --> SKIP NullPointer' % na
            continue
        print 'Show  %s  attributes' % na
        f.write("\r\n# %s\r\n\r\n" % na)
        f.flush()
        vs = AdminConfig.list(na).splitlines()
        for v in vs:
            f.write("\r\n## %s\r\n" % v)
            f.write(AdminConfig.show(v))
            f.write("\r\n")
        f.write("\r\n\r\n")
        f.flush()
    print "\ninfo file name %s\n" % fn
    f.close()

def get_summary():
    sp()
    get_cell()
    get_node()
    sp()
    get_servers()
    sp()
    get_j2c()
    sp()
    get_jdbcprovider()
    sp()
    get_datasource()
    sp()
    get_apps()
    sp()
    get_run_stat()
    sp()

def sp():
    print "\n\n%s" % ("--" * 35)

def get_cell():
    #name = AdminControl.getCell()
    cell = AdminConfig.list('Cell')
    name = AdminConfig.showAttribute(cell, 'name')
    print 'Cell: %s' % name

def get_node():
    #name = AdminControl.getNode()
    names = []
    for i in AdminConfig.list('Node').splitlines():
        names.append(AdminConfig.showAttribute(i, 'name'))
    print 'Node: %s' % "\t".join(names)

def get_servers():
    Dmgr = []
    Node = []
    Web = []
    Cluster = {}
    IndSer = []
    for serverx in AdminConfig.list('Server').splitlines():
        ts = AdminConfig.showAttribute(serverx, 'serverType')
        if ts == 'DEPLOYMENT_MANAGER':
            name = AdminConfig.showAttribute(serverx, 'name')
            Dmgr.append(name)
        elif ts == 'NODE_AGENT':
            name = AdminConfig.showAttribute(serverx, 'name')
            Node.append(name)
        elif ts == 'WEB_SERVER':
            name = AdminConfig.showAttribute(serverx, 'name')
            Web.append(name)
        elif ts == 'APPLICATION_SERVER':
            name = AdminConfig.showAttribute(serverx, 'name')

            jpd = AdminConfig.showAttribute(serverx, 'processDefinitions')[1:-1]  # [xxx]
            jvm = AdminConfig.showAttribute(jpd, 'jvmEntries')[1:-1]
            minh = AdminConfig.showAttribute(jvm, 'initialHeapSize') or ''
            maxh = AdminConfig.showAttribute(jvm, 'maximumHeapSize') or ''
            params = AdminConfig.showAttribute(jvm, 'genericJvmArguments') or ''
            JVM = [minh, maxh, params]

            svrs = AdminConfig.showAttribute(serverx, 'services')[1:-1].split()
            for i in svrs:
                if i.count('ThreadPoolManager'): thp = i; break
            pool = AdminConfig.showAttribute(thp, 'threadPools')[1:-1]
            for i in pool.split():
                if i.count('WebContainer'): webc = i
            mint = AdminConfig.showAttribute(webc, 'minimumSize') or ''
            maxt = AdminConfig.showAttribute(webc, 'maximumSize') or ''
            WEBT = [mint, maxt]

            apps = AdminConfig.showAttribute(serverx, 'components')[1:-1].split()
            for i in apps:
                if i.count('ApplicationServer'): app = i; break
            xx = AdminConfig.showAttribute(app, 'components')[1:-1].split()
            for i in xx:
                if i.count('WebContainer'): webc2 = i; break
            sm = AdminConfig.showAttribute(webc2, 'services')[1:-1]
            cook = AdminConfig.showAttribute(sm, 'defaultCookieSettings') or ''
            c_name = AdminConfig.showAttribute(cook, 'name') or ''
            c_age = AdminConfig.showAttribute(cook, 'maximumAge') or ''
            c_path = AdminConfig.showAttribute(cook, 'path') or ''
            c_sec = AdminConfig.showAttribute(cook, 'secure') or ''
            COOK = [c_name, c_path, c_age, c_sec]

            scfg = [name, COOK, JVM, WEBT]
            cln = AdminConfig.showAttribute(serverx, 'clusterName') or ''
            if cln:
                if not Cluster.has_key(cln):
                    Cluster[cln] = []
                Cluster[cln].append(scfg) #cont proc
            else:
                IndSer.append(scfg) #cont proc
        else:
            print 'Unknow serverType %' % ts

    print 'Dmgr:  %s' % "\t".join(Dmgr)
    print
    print 'Node:  %s' % "\t".join(Node)
    print
    print 'WebServer:  %s' % "\t".join(Web)
    print

    print 'Cluster: [name  JSession   genericJvmArguments    WebContainer]'
    cls = Cluster.keys()
    cls.sort()
    for clname in cls:
        print "    %s" % clname
        Cluster[clname].sort()
        for scfg in Cluster[clname]:
            print '        %s' % scfg[0]
            for i in range(1, len(scfg)):
                print '            %s' % "\t".join(scfg[i])
    print

    print 'Independent Server:'
    IndSer.sort()
    for scfg in IndSer:
        print '        %s' % scfg[0]
        for i in range(1, len(scfg)):
            print '            %s' % "\t".join(scfg[i])
    print

def get_j2c():
    J2C = []
    for j2c in AdminConfig.list('JAASAuthData').splitlines():
        alias = AdminConfig.showAttribute(j2c, 'alias') or ''
        uid = AdminConfig.showAttribute(j2c, 'userId') or ''
        pwd = AdminConfig.showAttribute(j2c, 'password') or ''
        desc =  AdminConfig.showAttribute(j2c, 'description') or ''
        J2C.append([alias, uid, pwd, desc])
    print 'JAASAuthData:'
    J2C.sort()
    for j2c in J2C:
        print "    %s" % "\t".join(j2c)

def get_jdbcprovider():
    JP = []
    for jp in AdminConfig.list('JDBCProvider').splitlines():
        classpath = AdminConfig.showAttribute(jp, 'classpath')
        if classpath.endswith('derby.jar'): continue #default
        name = AdminConfig.showAttribute(jp, 'name') or ''
        classn = AdminConfig.showAttribute(jp, 'implementationClassName') or ''
        typen = AdminConfig.showAttribute(jp, 'providerType') or ''
        JP.append([name, typen, classpath, classn])

    print 'JDBCProvidler: [name  type  classpath  classname]'
    JP.sort()
    for jp in JP:
        print '    %s' % "\t".join(jp)

def get_datasource():
    DS = []
    for ds in AdminConfig.list('DataSource').splitlines():
        name = AdminConfig.showAttribute(ds, 'name')
        jndi = AdminConfig.showAttribute(ds, 'jndiName') or ''
        auth = AdminConfig.showAttribute(ds, 'authDataAlias') or ''
        if auth is None: # not user datasource
            continue
        desc = AdminConfig.showAttribute(ds, 'description') or ''
        prov = AdminConfig.showAttribute(ds, 'provider') or ''
        provn = AdminConfig.showAttribute(prov, 'name') or ''
        TYPE = [jndi, auth, desc, provn]

        pool = AdminConfig.showAttribute(ds, 'connectionPool') or ''
        timeo = AdminConfig.showAttribute(pool, 'connectionTimeout') or ''
        utimeo = AdminConfig.showAttribute(pool, 'unusedTimeout') or ''
        minc = AdminConfig.showAttribute(pool, 'minConnections') or ''
        maxc = AdminConfig.showAttribute(pool, 'maxConnections') or ''
        POOL = [minc, maxc, timeo, utimeo]

        DS.append([name, TYPE, POOL])
    print 'DataSource: [jndi auth desc prov    minconn maxconn timeout unusedtimeout]'
    DS.sort()
    for ds in DS:
        print '    %s' % ds[0]
        for i in range(1, len(ds)):
            print '        %s' % "\t".join(ds[i])

def get_apps():
    apps = AdminApp.list().splitlines()
    apps.sort()
    APPCFG = []
    for app in apps:
        dep = AdminConfig.getid('/Deployment:%s/' % app)
        deploymentTargets = AdminConfig.showAttribute(dep, 'deploymentTargets')[1:-1]
        if '"' in deploymentTargets:    # app name has space char
            deploymentTargets = deploymentTargets.replace('" "', '"\n"').splitlines()
        else:
            deploymentTargets = deploymentTargets.split()
        DT = []
        for dt in deploymentTargets:
            name = AdminConfig.showAttribute(dt, 'name')
            DT.append(name)

        depobj = AdminConfig.showAttribute(dep, 'deployedObject') or ''
        binf = AdminConfig.showAttribute(depobj, 'useMetadataFromBinaries') or ''
        binurl = AdminConfig.showAttribute(depobj, 'binariesURL') or ''
        clsl = AdminConfig.showAttribute(depobj, 'classloader') or ''
        clslm1 = AdminConfig.showAttribute(clsl, 'mode') or ''
        mods = AdminConfig.showAttribute(depobj, 'modules')[1:-1] or ''
        if '"' in mods:
            mods = mods.replace('" "', '"\n"').splitlines()
        else:
            mods = mods.split()
        for i in mods:
            if i.count('WebModuleDeployment'): mods = i; break
        clslm2 = AdminConfig.showAttribute(mods, 'classloaderMode') or ''
        startorder = AdminConfig.showAttribute(depobj, 'startingWeight') or ''
        #cls3 = AdminConfig.showAttribute(mods, 'classloader')
        #clslm3 = AdminConfig.showAttribute(cls3, 'mode')
        ROOT = []
        JNDI = []
        vls = AdminApp.view(app).splitlines()
        re1 = re.compile('jndi.*jdbc',  re.I)
        re2 = re.compile(' /\w+$')
        for i in vls:
            if re1.search(i): JNDI.append(i)
            if re2.search(i): ROOT.append(i)
        CFG = [binf, binurl, clslm1, clslm2, startorder]
        APPCFG.append([app, DT, CFG, ROOT, JNDI])

    print "Applications: [name on_servers   binfile binurl cls1 cls2 startorder  ROOT  JNDI]"
    for cfg in APPCFG:
        print '    %s' % cfg[0]
        for i in range(1, len(cfg)):
            print '        %s' % "\t".join(cfg[i])

def get_run_stat():
    apps = AdminApp.list().splitlines()
    apps.sort()
    for app in apps:
        status = AdminControl.completeObjectName('type=Application,name=%s,*' % app)
        if status:
            pc = re.compile('process=(\w+),')
            pcs = pc.findall(status)
            stat = 'RUNNING %s' % '  '.join(pcs)
        else:
            stat = 'STOPPED'
        print '%-40s %s' % (app, stat)
    print 'Count: %d apps' % len(apps)

if __name__ == '__main__':
    cmds = ['create_all_help', 'create_attributes', 'get_all_info', 'get_summary']
    if len(sys.argv) < 1 or not sys.argv[-1] in cmds:
        print
        print "Syntax:"
        print "  wsadmin.bat -lang jython [ -conntype SOAP -host 127.0.0.1 -port 8879 ] -f utils.py CMD"
        print
        print '  CMD is one of:  ', "    ".join(cmds)
        sys.exit(1)
    cmd = eval(sys.argv[-1])
    cmd()

