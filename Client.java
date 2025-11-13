//客户端，与用户交互，向服务器发送请求并展示响应

package Server;
import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    //主方法，启动客户端并连接服务器进行交互
    //throws IOException当网络连接或IO操作发生错误时抛出
    public static void main(String[] args) throws IOException {
        //连接服务器
        Socket socket = new Socket("192.168.138.25", 8080);
        System.out.println("op已连接提瓦特大陆，可使用以下指令：");
        System.out.println("add 委托              （添加任务）");
        System.out.println("list                 （展示任务）");
        System.out.println("delete 委托ID         （删除任务）");
        System.out.println("exit                 （退出程序）");
        System.out.println("modify 委托ID 新委托   （修改任务）");
        System.out.println("complete 委托ID       （改变状态）");

        //获取输入流（接收）
        BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream(), "UTF-8")
        );

        //获取输出流（发送）
        PrintWriter out = new PrintWriter(
                new OutputStreamWriter(socket.getOutputStream(), "UTF-8"), true
        );

        //通信逻辑，循环读取用户输入并发送给服务器，等待服务器响应
        Scanner sc = new Scanner(System.in);
        String msg;
        while (true) {
            //读取用户指令
            msg = sc.nextLine();
            //发送到服务器
            out.println(msg);

            //若用户输入exit，接收服务器的退出提示并退出循环
            if ("exit".equals(msg)) {
                String exitMSG = in.readLine();     //在exit后没打印出想要的内容，而是直接退出，随后补充38，39
                System.out.println(exitMSG);
                break;
            }

            // 处理服务器回复
            if ("list".equals(msg)) {
                System.out.println("魔神任务：");
                // 使用while循环接收所有任务，直到收到END标志
                String response;
                while ((response = in.readLine()) != null) {
                    if ("------END------".equals(response)) {
                        break;
                    }
                    System.out.println(response);
                }
            }else {
                //有其他指令就打印服务器的单条回复
                System.out.println("服务器回复：" + in.readLine());
            }
        }
        //关闭资源
        sc.close();
        in.close();
        out.close();
        socket.close();
    }
}