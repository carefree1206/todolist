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
    public int getTaskID() {
        return taskID;
    }
    //获取任务内容
    public String getTaskCONTENT() {
        return taskCONTENT;
    }
    //修改任务内容，taskCONTENT是新的任务内容描述
    public void setTaskCONTENT(String taskCONTENT) {
        this.taskCONTENT = taskCONTENT;
    }
    //获取任务完成状态
    public boolean isOK(){
        return isOK;
    }
    //设置任务完成状态
    public void setOK(boolean OK){
        isOK = OK;
    }
    //切换任务完成状态
    public void change(){
        isOK = !isOK;
    }

//格式化信息后展示
    public String Show() {

        String done;
        if (isOK) {
            done = "【已完成】";
        } else {
            done = "【未完成】";
        }
        return this.taskID + ":" + this.taskCONTENT + "（我想进自科部！！！）" + done;
    }
}