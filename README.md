使用AssociationRule、HCP、Distance 方法步骤
1、需要先使用命令
git log  --pretty=format:'commit %H(%ad)%nauthor:%an%ndescription:%s'  --date=format:'%Y-%m-%d %H:%M:%S'    --numstat  --name-status  --reverse --no-merges >master.txt
获取项目的 commit history ，到master.txt文件中


2、使用命令 main.py  --filePath --method --support --confidence --IndexDistance --TimeDistance

--filePath 是master.txt文件的文件路径
--method 可以为HCP、AsociationRule、Distance
--support 设置的支持度的值
--confidence 置信度
--IndexDistance 使用Distance 方法时要设置的commit Index的距离
--TimeDistance  使用Distance 方法时要设置的commit Time的距离 （以小时为单位）

3、生成的结果以JSON文件保存，与master.txt在同一目录下


使用follow 方法步骤
1、使用命令 main.py  --filePath --method --support --confidence 

--filePath 是项目路径
--method 设置为follow
--support 设置的支持度的值
--confidence 置信度


2、生成的结果以JSON文件保存，在项目路径下
