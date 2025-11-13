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
    public void addTask(String taskCONTENT){
        // 创建新任务对象并添加到链表（ID自动递增）
        taskList.add(new Task(taskID++, taskCONTENT));
    }
    //get和show都是用以实现list功能（获取+打印）
    //返回储存所有Task对象的LinkedList
    public LinkedList<Task> getTasks() {
        return taskList;
    }
    //在服务器控制台打印所有委托信息，用以服务器调试
    public boolean showTask()
    {
        for (Task task : taskList)
        {
            System.out.println(task.Show());
        }
        return false;
    }
    //删除功能，删除成功返回ture，删除失败返回false
    public boolean deleteTask(int taskID){
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
    public boolean modifyTask(int taskID,String newCONTENT){
        for (Task task : taskList) {
            if (task.getTaskID() == taskID) {
                task.setTaskCONTENT(newCONTENT);
                return true;
            }
        }
        return false;
    }
}