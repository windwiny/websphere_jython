import sys
import os

sys.exit(0)


flag
#'nd'

AdminControl.getHost()
#'localhost'
AdminControl.getPort()
#'8879'
AdminControl.getType()
#'SOAP'

# ��Ԫ\�ڵ���
AdminControl.getCell()
#'vbox001Cell01'
AdminControl.getNode()
#'vbox001CellManager01'

# �г��ڵ�
# [13-6-12 13:05:04:529 CST] Node
AdminTask.listNodes()
#'vbox001CellManager01\r\nvbox001Node01'
# vbox001CellManager01
# vbox001Node01

#=begin  ͨ�ò�ѯʾ��
# �г�ȫ����������
AdminConfig.types().splitlines() # ���ض����ַ���  TYPE_XXX TYPE_YYY ...
# Cell  => 1��
# Node  => ��� Manager Node01 02 ..
# NodeAgent =>
# Server => dmgr+web+server
# ServerCluster => cluster
# ApplicationServer => appserver
# WebServer => webserver
# JDBCProvider =>
# DataSource  => 
# Deployment  => deploymented applications == AdminApp.list().each {|x|  AdminConfig.getid('/Deployment:' + x + '/') }
# DeployedObject  =>  AdminConfig.showAttribute(deployment_xxx, 'deployedObject')
# DeployedTarget  =>
# HostAlias VirtualHost ApplicationServer Application  
# SessionManager =>
# Cookie =>
# ...

# �г�ĳ������������� [_attributes.txt]
AdminConfig.attributes(TYPE_XXX).splitlines()  # ���ض�� ������ ��
# attributename_xxx  Class(X1)
# attributename_yyy  Class(Y1)
# ...

AdminConfig.required(TYPE_XXX).splitlines()  # �г�ĳ������������
AdminConfig.defaults(TYPE_XXX)
# ...

AdminConfig.list(TYPE_XXX).splitlines()  # ����ȫ��ָ�������
# idxxx    =>  name_xxx(xx/yy/zz.xml#id)
# idyyy
# ...

AdminConfig.getid('/TYPE_XXX:name_xxx/') # ����������id,��AdminConfig.list().splitlines()���ص���ͬ
# idxxx

AdminConfig.showAttribute(idxxx, attributename_xxx) # ȡ������
# instance_x1  => Class(X1)'s object

AdminConfig.show(instance_x1).splitlines() # ��ʾȫ������
# ...

AdminConfig.modify(idxxx, [['key', 'value'], ]  # �޸�����

AdminConfig.save() # ����
AdminConfig.reset() # ��������,�ָ����ϴα���
AdminConfig.remove(idxxx) # ɾ��
#=end

# �г�������\��Ⱥ\web������
AdminConfig.list('Server')
# dmgr(cells/vbox001Cell01/nodes/vbox001CellManager01/servers/dmgr|server.xml#Server_1)
# nodeagent(cells/vbox001Cell01/nodes/vbox001Node01/servers/nodeagent|server.xml#Server_1371010325491)
# server1(cells/vbox001Cell01/nodes/vbox001Node01/servers/server1|server.xml#Server_1183122130078)
# server2(cells/vbox001Cell01/nodes/vbox001Node01/servers/server2|server.xml#Server_1371012141191)
# webserver1(cells/vbox001Cell01/nodes/vbox001Node01/servers/webserver1|server.xml#Server_1371010463499)
AdminConfig.list('ServerCluster')
# ''
AdminConfig.list('WebServer')
#'webserver1(cells/vbox001Cell01/nodes/vbox001Node01/servers/webserver1|server.xml)'
# -or-
# [13-6-12 12:30:31:481 CST] ApplicationServer
AdminTask.listServers('[-serverType APPLICATION_SERVER ]') 

# [13-6-12 12:31:56:824 CST] ServerCluster
AdminConfig.list('ServerCluster', AdminConfig.getid( '/Cell:vbox001Cell01/'))

# [13-6-12 12:58:03:008 CST] WebServer
AdminTask.listServers('[-serverType WEB_SERVER ]')




# �г����������˿� [�������˿�]
# [13-6-12 13:12:47:139 CST] �������� > default_host
AdminConfig.list('HostAlias', AdminConfig.getid( '/Cell:vbox001Cell01/VirtualHost:default_host/'))
#'(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334614)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334674)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334764)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334784)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334814)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334834)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_2)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_3)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_6)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_7)\r\n(cells/vbox001Cell01|virtualhosts.xml#HostAlias_8)'
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334614)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334674)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334764)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334784)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334814)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_1371010334834)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_2)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_3)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_6)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_7)
# (cells/vbox001Cell01|virtualhosts.xml#HostAlias_8)

# ������ʹ�õĶ˿�
AdminTask.reportConfiguredPorts()
#...

# ���web�������Ƿ�����
# [13-6-12 12:58:03:258 CST] Web ������
AdminControl.invoke('WebSphere:name=WebServer,process=dmgr,platform=common,node=vbox001CellManager01,version=7.0.0.15,type=WebServer,mbeanIdentifier=WebServer,cell=vbox001Cell01,spec=1.0', 'ping', '[vbox001Cell01 vbox001Node01 webserver1]', '[java.lang.String java.lang.String java.lang.String]')
#'RUNNING'

# �г��������µ�Ӧ��
# [13-6-12 13:04:00:071 CST] Ӧ�ó�������� > server1
AdminApp.list("WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=server2")
#'DefaultApplication.ear'


# ��ʾȫ��Ӧ��
# [13-6-12 12:44:25:881 CST] ApplicationDeployment
AdminApp.list()
#'DefaultApplication.ear'

# �鿴�Ƿ�����
AdminControl.completeObjectName('type=Application,name=XXXXXX,*') #XXX ΪӦ����,���������з���

# �鿴Ӧ��������Ϣ
AdminApp.view(XXX)

# ��װӦ��

# [13-6-12 12:37:56:781 CST] ��ҵӦ�ó��� > ��ҵӦ�ó���
AdminApp.install('D:/IBM/WebSphere/AppServer/profiles/Dmgr01/config/temp/upload/1371011849933/DefaultApplication.ear', '[  -nopreCompileJSPs -installed.ear.destination /wlsapp -distributeApp -useMetaDataFromBinary -nodeployejb -appname DefaultApplication.ear -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -MapModulesToServers [[ "Increment EJB module" Increment.jar,META-INF/ejb-jar.xml WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=server1+WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=webserver1 ][ "Default Web Application" DefaultWebApplication.war,WEB-INF/web.xml WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=server1+WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=webserver1 ]]]' )

# [13-6-12 12:38:01:358 CST] ��ҵӦ�ó��� > ��ҵӦ�ó���
AdminConfig.save()

# [13-6-12 12:38:02:009 CST] ��ҵӦ�ó��� > ��ҵӦ�ó���
AdminControl.invoke('WebSphere:name=DeploymentManager,process=dmgr,platform=common,node=vbox001CellManager01,diagnosticProvider=true,version=7.0.0.15,type=DeploymentManager,mbeanIdentifier=DeploymentManager,cell=vbox001Cell01,spec=1.0', 'multiSync', '[false]', '[java.lang.Boolean]')

#AdminApp.options()
#AdminApp.install('xx.ear', [-opt val -opt val])


# �޸Ĺ���ģ�� ������
# [13-6-12 12:45:04:176 CST] ��ҵӦ�ó��� > DefaultApplication.ear > ����ģ��
AdminApp.edit('DefaultApplication.ear', '[  -MapModulesToServers [[ "Increment EJB module" Increment.jar,META-INF/ejb-jar.xml WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=webserver1+WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=server2 ][ "Default Web Application" DefaultWebApplication.war,WEB-INF/web.xml WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=webserver1+WebSphere:cell=vbox001Cell01,node=vbox001Node01,server=server2 ]]]' )

# [13-6-12 12:45:27:449 CST] ��ҵӦ�ó��� > DefaultApplication.ear
AdminConfig.save()

# [13-6-12 12:45:28:090 CST] ��ҵӦ�ó��� > DefaultApplication.ear
AdminControl.invoke('WebSphere:name=DeploymentManager,process=dmgr,platform=common,node=vbox001CellManager01,diagnosticProvider=true,version=7.0.0.15,type=DeploymentManager,mbeanIdentifier=DeploymentManager,cell=vbox001Cell01,spec=1.0', 'multiSync', '[false]', '[java.lang.Boolean]')


# ����Ӧ��
# [13-6-12 12:46:23:290 CST] ��ҵӦ�ó���
AdminControl.invoke('WebSphere:name=ApplicationManager,process=server2,platform=proxy,node=vbox001Node01,version=7.0.0.15,type=ApplicationManager,mbeanIdentifier=ApplicationManager,cell=vbox001Cell01,spec=1.0', 'startApplication', '[DefaultApplication.ear]', '[java.lang.String]')


# �޸�Ӧ�ø�·��

# [13-6-12 14:20:59:263 CST] ��ҵӦ�ó��� > DefaultApplication.ear > Web ģ��������ĸ�
AdminApp.edit('DefaultApplication.ear', '[  -CtxRootForWebMod [[ "Default Web Application" DefaultWebApplication.war,WEB-INF/web.xml /cc ]]]' )

# [13-6-12 14:21:01:536 CST] ��ҵӦ�ó��� > DefaultApplication.ear
AdminConfig.save()

# [13-6-12 14:21:01:887 CST] ��ҵӦ�ó��� > DefaultApplication.ear
AdminControl.invoke('WebSphere:name=DeploymentManager,process=dmgr,platform=common,node=vbox001CellManager01,diagnosticProvider=true,version=7.0.0.15,type=DeploymentManager,mbeanIdentifier=DeploymentManager,cell=vbox001Cell01,spec=1.0', 'multiSync', '[false]', '[java.lang.Boolean]')


# �����˳��
dep = AdminConfig.getid("/Deployment:DefaultApplication/")
depObject = AdminConfig.showAttribute(dep, 'deployedObject')
classldr = AdminConfig.showAttribute(depObject, 'classloader')
AdminConfig.showall(classldr)
#'DefaultApplication(cells/vbox001Cell01/applications/DefaultApplication.ear/deployments/DefaultApplication|deployment.xml#Deployment_1370494919349)'
#'(cells/vbox001Cell01/applications/DefaultApplication.ear/deployments/DefaultApplication|deployment.xml#ApplicationDeployment_1370494919349)'
#'(cells/vbox001Cell01/applications/DefaultApplication.ear/deployments/DefaultApplication|deployment.xml#Classloader_1370494919349)'
#'[libraries []]\r\n[mode PARENT_LAST]'

## AdminConfig.modify(classldr, [['mode', 'PARENT_LAST']])

# ����˳��
AdminConfig.show(depObject, 'startingWeight')
#'[startingWeight 1]'
## AdminConfig.modify(depObject, [['startingWeight', '2']])


# ͬ���ڵ�?
node_ids = AdminConfig.list("Node").splitlines() 
for node in node_ids:
    nodename = AdminConfig.showAttribute(node,"name")
    nodesync = AdminControl.completeObjectName("type=NodeSync,node=" + nodename + ",*") 
    if nodesync != "":
        AdminControl.invoke(nodesync,"sync")


[db2admin db2inst1 db2inst2 db2inst3 cell dccell rone rone4  hsyymis tso tc yy_pub yy_sc yy_sg yy_db yy_fk yy_ca r1 yyinfo yyintotm ]
[oracle system tsoadmin celladmin yymisadmin]

