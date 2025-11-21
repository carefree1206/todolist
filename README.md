[README.md](https://github.com/user-attachments/files/23676076/README.md)[Uploading RE# ToDoList 系统说明文档
- 文档作者：吴兴明
- 技术方向：自科部后端方向
- 核心重点：**三最重要（原文强调，需重点关注）**
- 系统架构：基于 多线程的Socket 的客户端-服务器（C/S）模式，控制台交互，模拟原神委托任务管理


## 一、项目架构
### 1. 功能说明
封装单个任务的核心信息，作为数据载体在 Client、Server、LinkedListTM 模块间传递，支持任务完成状态切换与格式化信息展示。

### 2. 设计要点
- 数据封装：私有成员变量 + getter/setter 方法，禁止直接修改属性；
- 默认状态：任务创建时默认“未完成”，通过 `setCompleted()` 方法切换状态；
- 格式适配：重写 `toString()` 方法，按“原神委托”风格输出任务信息。

### 3. 模块介绍
1. **Client（客户端）**  
功能：与用户交互，接收用户指令并发送至服务器，展示服务器返回的响应结果。
设计：
- add（添加任务）           
  ```add <任务内容>```
- list（查询任务）          
  ```list```
- modify（修改任务）        
  ```modify <任务ID> <新任务内容>```
- delete（删除任务）        
  ```delete <任务ID>```
- exit（退出系统）          
  ```exit```
- complete（标记任务完成）  
  ```complete <任务ID>```
```java
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
        Socket socket = new Socket("127.0.0.1", 10086);
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
```
1. **Server（服务器）**
功能：持续监听客户端连接，每接收一个连接便开启独立线程处理，将用户的任务操作需求分发至对应功能模块。
设计：
- 通过线程池实现多客户端同时使用。
- 所有客户端共享一个任务列表，保证数据同步。
- 具备指令识别能力，输入错误指令时会给出提示。
```java
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
        ServerSocket server = new ServerSocket(10086);
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
                        out.println("ID"+"\t"+"完成情况"+"\t\t"+"taskCONTENT");
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
```
3. **LinkedListTM（任务管理模块）**
功能：负责任务的核心操作，包括添加、删除、修改、查询，采用 LinkedList 存储任务数据。
设计：
- 利用 LinkedList 存储单个任务对象。
- 任务 ID 自动递增，确保唯一性。
- 添加了synchronized作为线程锁确保了线程安全。
```java
package tools;

import java.util.LinkedList;

//任务管理类（add delete list modify）
public class LinkedListTM {

    //存储任务的链表容器
    private LinkedList<Task> taskList;
    //未使用的状态标记
    private boolean isOver;
    //任务ID自增计数器
    private int taskID = 1;

    //初始化任务链表
    public LinkedListTM(){
        taskList = new LinkedList<>();
    }
    //添加任务，taskCONTENT是委托的具体内容描述
    public synchronized void addTask(String taskCONTENT){
        // 创建新任务对象并添加到链表（ID自动递增）
        taskList.add(new Task(taskID++, taskCONTENT));
    }
    //get和show都是用以实现list功能（获取+打印）
    //返回储存所有Task对象的LinkedList
    public synchronized LinkedList<Task> getTasks() {
        return taskList;
    }
    //在服务器控制台打印所有委托信息，用以服务器调试
    public synchronized boolean showTask()
    {
        System.out.println("ID"+"\t"+"完成情况"+"\t\t"+"taskCONTENT");
        for (Task task : taskList)
        {
            System.out.println(task.Show());
        }
        return false;
    }
    //删除功能，删除成功返回ture，删除失败返回false
    public synchronized boolean deleteTask(int taskID){
        //从后往前遍历链表
        for (int i = taskList.size() - 1; i >= 0; i--) {
            Task task = taskList.get(i);
            if (task.getTaskID() == taskID) {
                taskList.remove(i);
                return true;
            }
        }
        return false;
    }
    //修改功能，修改成功返回ture，修改失败返回false
    //taskID要修改委托的ID；newCONTENT新的任务内容描述
    public synchronized boolean modifyTask(int taskID,String newCONTENT){
        for (Task task : taskList) {
            if (task.getTaskID() == taskID) {
                task.setTaskCONTENT(newCONTENT);
                return true;
            }
        }
        return false;
    }
}
```
4. **Task（任务实体）**
功能：存储单个任务的信息（ID、任务内容、完成状态），支持完成状态切换操作。
设计：
- 采用数据封装，通过 getter/setter 方法控制数据访问。
- 内置状态切换和信息展示方法。
- 添加了synchronized作为线程锁确保了线程安全。
```java
package tools;

//任务实体类Task，封装ID,CONTENT,完成状态
public class Task {
    //任务ID
    private int taskID;
    //任务内容
    private String taskCONTENT;
    //完成状态
    private boolean isOK;

    //创建方法，初始化
    public Task(int taskID, String taskCONTENT){
        this.taskID = taskID;           //委托标识ID
        this.taskCONTENT = taskCONTENT; //委托内容
        //创建时默认未完成
        this.isOK = false;
    }
    //getter和setter方法
    //获取委托ID
    public synchronized  int getTaskID() {
        return taskID;
    }
    //获取任务内容
    public synchronized String getTaskCONTENT() {
        return taskCONTENT;
    }
    //修改任务内容，taskCONTENT是新的任务内容描述
    public synchronized void setTaskCONTENT(String taskCONTENT) {
        this.taskCONTENT = taskCONTENT;
    }
    //获取任务完成状态
    public synchronized boolean isOK(){
        return isOK;
    }
    //设置任务完成状态
    public synchronized void setOK(boolean OK){
        isOK = OK;
    }
    //切换任务完成状态
    public synchronized void change(){
        isOK = !isOK;
    }

//格式化信息后展示
    public synchronized  String Show() {

        String done;
        if (isOK) {
            done = "【已完成】";
        } else {
            done = "【未完成】";
        }
        return this.taskID + "\t" + done + '\t' + this.taskCONTENT+ "（我想进自科部！！！）";
    }
}
```

## 二、模块使用
- add（添加任务）           
  ```add <任务内容>```
- list（查询任务）          
  ```list```
- modify（修改任务）        
  ```modify <任务ID> <新任务内容>```
- delete（删除任务）        
  ```delete <任务ID>```
- exit（退出系统）          
  ```exit```
- complete（标记任务完成）  
  ```complete <任务ID>```

## 三、设计历程
（开始写程序时，从舍友口中得知程序员炒饭的故事，故特别注重对错误输入的处理）

1. **初期规划：核心类搭建**  
首先规划创建两个核心类，分别承载任务数据与操作逻辑：  
- `Task`（任务实体类）：负责描述单个任务的具体信息，初期仅封装 **ID** 和 **CONTENT** 两个字段；  
- `LinkedListTM`（任务管理模块）：通过各类指令操作 `Task` 对象，优先实现 `add` 方法，确保任务添加功能正常后，再逐步完善其他功能。


2. **通信实现：Socket 模块开发**  
随后借助 AI 学习 Socket 通信知识，完成客户端（Client）与服务器（Server）模块的基础搭建，实现二者双向数据传输。  
- 初期在服务器模块处理 `add` 指令时，使用 `("add".equals(msg))` 进行判断，无法识别 “add + 任务内容” 的完整格式；  
- 后续将判断逻辑改为 `msg.startsWith("add")`，成功识别带内容的指令，试运行通过。


3. **体验优化：指令提示与方法完善**  
发现客户端缺乏指令格式引导，补充以下优化：  
- 客户端连接成功后，自动打印所有支持的指令格式及用途（当时规划了 `add`、`list`、`delete`、`exit` 四类指令），同时在 `LinkedListTM` 中补充对应实现方法；  
- 实现 `list` 方法时，初期仅在服务器端打印任务，客户端无响应，后续通过 `for` 循环遍历所有任务并逐行传输至客户端，用 **“------END------”** 作为传输结束标志，确保客户端完整接收；  
- 设计 `exit` 方法时，原本直接用 `break` 退出，后来增加自定义反馈信息（如“已安全断开连接”）并传输至客户端，提升用户感知。


4. **功能补全：异常处理与漏洞修复**  
完成初期开发后，发现遗漏 `modify`（修改任务）功能，补充实现后进入测试阶段，解决关键问题：  
- 测试中发现，当客户端输入错误指令（如将 `add` 误输为 `ass`）时，客户端会陷入无响应状态，需重新连接服务器；  
- 针对该问题，在 Client 模块添加 `else` 逻辑：识别到非预设指令时，立即向客户端发送“指令格式错误，请重新输入”的提醒，且不中断当前连接，不影响后续操作。


5. **功能扩展：原神化设计收尾**  
受错误指令处理优化的启发，新增“任务完成状态切换”功能（即 `complete` 指令）。  
- 最后开发阶段，因舍友正在玩原神，联想到“原神委托任务”与 ToDoList 的功能逻辑相似，遂将程序进行原神化设计（如将“任务”表述改为“委托”，响应提示改为“委托已添加”“委托完成”等），增强使用趣味性。ADME.md…]()
