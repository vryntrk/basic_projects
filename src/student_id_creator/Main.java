package homework;

public class Main {
    public static void main(String[] args) {
        StudentIdCreator studentId1 = new StudentIdCreator();
        studentId1.name = "Seher";
        studentId1.surname = "Yıldız";
        studentId1.departmentName = "Computer Engineering";
        studentId1.entryYear = "2022";
        studentId1.setDepartment("Computer Engineering");
        studentId1.entryOrder = "104";

        System.out.println(studentId1);

        StudentIdCreator studentId2 = new StudentIdCreator();
        studentId2.name = "Cahit";
        studentId2.surname = "Arf";
        studentId2.departmentName = "Mathematics";
        studentId2.entryYear = "2024";
        studentId2.setDepartment("Mathematics");
        studentId2.entryOrder = "001";

        System.out.println(studentId2);

        StudentIdCreator studentId3 = new StudentIdCreator();
        studentId3.name = "Deniz";
        studentId3.surname = "Alabora";
        studentId3.departmentName = "Biology";
        studentId3.entryYear = "2025";
        studentId3.setDepartment("Biology");
        studentId3.entryOrder = "025";

        System.out.println(studentId3);
    }
}
