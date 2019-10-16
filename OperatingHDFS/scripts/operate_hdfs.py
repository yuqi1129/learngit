# -*- coding:utf-8 -*-
# author:wenbin
# datetime:2019/10/15 17:44

import subprocess as sp


class OperateHDFS:
    def view_file(self, file_path):
        '''
        查看文件内容
        :param file_path: 文件路径(绝对路径)
        :return: 标准输出的文件内容
        '''

        content = sp.Popen('/opt/soft/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs -cat ' + file_path, shell=True,
                           stdout=sp.PIPE, stderr=sp.PIPE)
        return {'stdout': content.stdout.read().decode('utf-8'), 'stderr': content.stderr.read().decode('utf-8')}


if __name__ == '__main__':
    tes = OperateHDFS()
    file_path = '/user/h_data_platform/arbiter_staging/tasks/date=20191011/task-78/stdout'
    print(tes.view_file(file_path))
