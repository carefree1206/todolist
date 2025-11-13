//服务器端，负责监听客户端连接，处理客户端的任务管理请求

package Server;

import tools.LinkedListTM;
import tools.Task;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    //静态任务链表，用于存储所有客户端共享的任务列表
    static LinkedListTM list = new LinkedListTM();
    //启动服务器端，并监听客户端连接
    public static void main(String[] args) throws IOException {
        //初始化服务器socket，绑定端口8080
        ServerSocket server = new ServerSocket(8080);
        System.out.println("原神启动，等待op连接...");

        //循环接收多个客户端连接（主线程只负责监听，不处理具体通信）
        while (true) {
            //阻塞等待新客户端连接
            Socket socket = server.accept();
            System.out.println("op已连接：" + socket.getLocalAddress().getHostName());

            //为每个客户端创建独立线程处理通信，避免单客户端阻塞影响其他客户端
            new Thread(new ClientHandler(socket)).start();
        }
    }

    // 内部类：专门处理单个客户端的通信逻辑（实现Runnable接口）
    static class ClientHandler implements Runnable {
        private Socket socket; // 当前客户端的Socket连接

        //初始化客户端服务器
        public ClientHandler(Socket socket) {
            this.socket = socket;   //客户端连接的Socket对象
        }

        public void run() {
            //初始化，为当前客户端处理输入输出流
            try (
                    BufferedReader in = new BufferedReader(
                            new InputStreamReader(socket.getInputStream(), "UTF-8")
                    );
                    PrintWriter out = new PrintWriter(
                            new OutputStreamWriter(socket.getOutputStream(), "UTF-8"), true
                    )
            ) {
                //与当前客户端的通信循环
                String msg;
                while ((msg = in.readLine()) != null) {
                    System.out.println("op[" + socket.getPort() + "]发送：" + msg);
                    //out.println("服务器已收到：" + msg); 响应客户端（客户端会收到该指令）（这段导致运行时要回车两次才能在客户端显示下面的内容）
                    //若需要显示上方内容同时解决此bug，可在Client内使用while循环接收服务器的所有回复
                    //实现交互逻辑
                    if (msg.startsWith("add ")) {
                        // 处理add指令 添加任务（add 任务内容）
                        String content = msg.substring(4);
                        if (!content.isEmpty()) {
                            list.addTask(content);
                            out.println("叮咚您有委托未完成");
                        } else {
                            out.println("没有委托任务");
                        }
                    }
                    //处理list指令
                    else if ("list".equals(msg)) {
                        list.showTask();//原本只写了这一行来展示待办事项，运行后改进
                        for(Task task : list.getTasks()){
                            out.println(task.Show());
                        }
                        out.println("------END------");
                    }
                    //处理exit指令
                    else if ("exit".equals(msg)) {
                        out.println("期待下次与您在自科部相见，遨游提瓦特大陆！！！");
                        break;//退出通信循环
                    }
                    //处理delete指令
                    else if(msg.startsWith("delete ")){
                        String idStr = msg.substring(7).trim();  // 提取ID部分
                        if (idStr.isEmpty()) {
                            out.println("请输入要删除的委托ID（格式：delete 委托ID）");
                            continue;
                        }
                        try {
                            int taskId = Integer.parseInt(idStr);
                            boolean isDeleted = list.deleteTask(taskId);
                            if (isDeleted) {
                                out.println("委托ID " + taskId + " 已成功删除");
                            } else {
                                out.println("未找到ID为 " + taskId + " 的委托");
                            }
                        } catch (NumberFormatException e) {
                            out.println("请输入有效的数字ID");
                        }
                    }
                    //处理modify指令
                    else if (msg.startsWith("modify ")) {
                        String part = msg.substring(7).trim();
                        if (part.isEmpty()) {
                            out.println("请输入要修改的委托ID和新内容（格式：modify 委托ID 新内容）");
                            continue;
                        }
                        //分割ID与新内容
                        String[] parts = part.split(" ", 2);
                        if (parts.length < 2) {
                            out.println("格式错误，请使用：modify 委托ID 新内容");
                            continue;
                        }
                        String idStr = parts[0].trim();
                        String newContent = parts[1].trim();
                        if (newContent.isEmpty()) {
                            out.println("新内容不能为空");
                            continue;
                        }
                        try {
                            int taskId = Integer.parseInt(idStr);
                            boolean isModified = list.modifyTask(taskId, newContent);
                            if (isModified) {
                                out.println("委托ID " + taskId + " 已成功修改");
                            } else {
                                out.println("未找到ID为 " + taskId + " 的委托");
                            }
                        } catch (NumberFormatException e) {
                            out.println("请输入有效的数字ID");
                        }
                    }
                    // 处理"complete"指令：切换指定ID任务的完成状态
                    else if (msg.startsWith("complete ")) {
                        String idStr = msg.substring(9).trim();
                        if (idStr.isEmpty()) {
                            out.println("请输入要标记的委托ID（格式：complete 委托ID）");
                            continue;
                        }
                        try {
                            int taskId = Integer.parseInt(idStr);
                            //查找任务并切换状态
                            boolean found = false;
                            // 遍历任务列表查找指定ID的任务并切换状态
                            for (Task task : list.getTasks()) {
                                if (task.getTaskID() == taskId) {
                                    task.change();  // 切换完成状态
                                    found = true;
                                    if (task.isOK()) {
                                        out.println("委托ID " + taskId + " 已标记为【已完成】");
                                    } else {
                                        out.println("委托ID " + taskId + " 已标记为【未完成】");
                                    }
                                    break;
                                }
                            }
                            if (!found) {
                                out.println("未找到ID为 " + taskId + " 的委托");
                            }
                        } catch (NumberFormatException e) {
                            out.println("请输入有效的数字ID");
                        }
                    }
                    //运行时经常打错字母，导致程序无法继续，故写出以下代码（输入上面操作之外的东西会执行）
                    //处理未知指令
                    else{
                        out.println("无此功能，请重新输入");
                    }
                }
            } catch (IOException e) {
                System.out.println("op[" + socket.getPort() + "]连接异常：" + e.getMessage());
            } finally {
                //关闭当前客户端的连接资源
                try {
                    socket.close();
                    System.out.println("op[" + socket.getPort() + "]已断开连接");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}