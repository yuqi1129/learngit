# -*- coding:utf-8 -*-
# author:wenbin
# datetime:2019/10/14 16:10

from hdfs.ext.kerberos import KerberosClient


class OperateHDFS:
    def __init__(self, url):
        '''

        :param url:HDFS名称节点的主机名或IP地址,以协议为前缀,其次是namenode上的WebHDFS端口,也可以指定多个URL以分号分隔以获取高可用性支持.
        '''
        # 实例化HDFS web client using Kerberos authentication
        self.client = KerberosClient(url)

    def file_list(self, file_path):
        '''

        :param file_path: HDFS远程目录路径
        :return: 返回一个远程目录中包含的所有文件
        '''
        file_detail = self.client.list(hdfs_path=file_path)
        return file_detail

    def file_read(self, file_path):
        '''
        从HDFS中读取文件
        :param file_path: HDFS远程文件路径
        :return:
        '''
        lines = []
        with self.client.read(hdfs_path=file_path, encoding='utf-8', delimiter=r'\n') as reader:
            # content = file.read()
            # print(content)
            for item in reader:
                lines.append(item.strip())
        return lines

    def file_create_write(self, file_path, data_write):
        '''
        在HDFS中创建新文件并写入内容
        :param file_path: HDFS远程文件路径
        :param data_write: 写入到文件的数据
        :return:
        '''
        self.client.write(hdfs_path=file_path, data=data_write, encoding='utf-8')

    def file_append_write(self, file_path, data_append):
        '''
        在HDFS中已存在的文件中追加写入内容，文件必须已存在
        :param file_path: HDFS远程文件路径
        :param data_append: 追加到文件的数据
        :return:
        '''
        self.client.write(hdfs_path=file_path, data=data_append, encoding='utf-8', append=True)

    def file_rename(self, src_file_path, dst_file_path):
        '''
        重命名/移动文件或文件夹
        :param src_file_path: 源文件路径
        :param dst_file_path: 目的文件路径
        :return:
        '''
        self.client.rename(hdfs_src_path=src_file_path, hdfs_dst_path=dst_file_path)

    def mkdir(self, file_path):
        '''
        在HDFS中创建远程目录，必要时递归创建
        :param file_path: 需要新建的文件夹路径(包含名字)
        :return:
        '''
        self.client.makedirs(hdfs_path=file_path)

    def upload_files(self, file_path, local_path):
        '''
        上传文件或目录到HDFS
        :param file_path:HDFS目标路径。如果它已经存在并且是一个目录，文件将被上传其中。
        :param local_path:文件或文件夹的本地路径。 如果是文件夹，则将上传其中的所有文件（请注意，这意味着没有文件的文件夹将不会远程创建）
        :return:hdfs_path_return:成功后，此方法将返回远程上传路径。
        '''
        hdfs_path_return = self.client.upload(hdfs_path=file_path, local_path=local_path)
        return hdfs_path_return

    def download_files(self, file_path, local_path):
        '''
        从HDFS下载一个文件或文件夹并将其保存在本地
        :param file_path:HDFS上要下载的文件或文件夹的路径。 如果是文件夹，则将下载该文件夹下的所有文件
        :param local_path:本地路径。 如果它已经存在并且是目录，则文件将在其中下载。
        :return: local_path_return:成功后，此方法将返回本地下载路径
        '''
        local_path_return = self.client.download(hdfs_path=file_path, local_path=local_path)
        return local_path_return

    def delete_files(self, file_path):
        '''
        从HDFS中删除文件或目录
        :param file_path: HDFS中需要删除的文件或目录的路径
        :return:如果删除成功，则此函数返回“ True”，如果先前在“ hdfs_path”处不存在文件或目录，则返回“ False”。
        '''
        # recursive：递归删除文件和目录。 默认情况下，如果尝试删除非空目录，则此方法将引发HdfsError。
        # skip_trash：设置为false时，已删除的路径将被移至相应的垃圾文件夹，而不是被删除。 这需要Hadoop 2.9+且在集群上启用trash
        return self.client.delete(hdfs_path=file_path, recursive=False, skip_trash=True)

    def set_files_permission(self, file_path):
        '''
        更改文件的权限
        :param file_path: 需要更改权限的文件路径
        :return:
        '''
        # permission：文件的新八进制权限字符串
        self.client.set_permission(hdfs_path=file_path, permission=None)