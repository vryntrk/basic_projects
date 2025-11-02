package homework;

public class StudentIdCreator {
    String name;
    String surname;
    String departmentName;
    String entryYear;
    String departmentCode;
    String entryOrder;

    public void setDepartment(String value) {
        if(value == "Computer Engineering") {
            this.departmentCode = "356";
        }
        else if(value == "Mathematics") {
            this.departmentCode = "328";
        }
        else{
            System.out.println("There Is No Code For The " + departmentName + " Department. Please Try Again Later.");
            System.exit(1);
        }
    }

    public String getDepartment() {
        return departmentCode;
    }

    @Override
    public String toString() {
        return "Student Informations: [" +
                "Name: " + name +
                ", Surname: " + surname +
                ", Department: " + departmentName +
                ", ID:" + entryYear + getDepartment() + entryOrder +
                "]";
    }
}
