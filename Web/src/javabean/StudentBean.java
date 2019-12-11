package javabean;

import java.util.Calendar;

public class StudentBean {
	private String id;		//ID
	private String name;	//이름
	private String snum;	//학번
	private int year;		//생년
	private String pass;	//암호
	private String email;	//전자메일
	
	//메뉴 [source]/[Generate Getter and Setters …]를 이용 자동 생성
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getSnum() {
		return snum;
	}
	public void setSnum(String snum) {
		this.snum = snum;
	}
	public int getYear() {
		return year;
	}
	public void setYear(int year) {
		this.year = year;
	}
	public String getPass() {
		return pass;
	}
	public void setPass(String pass) {
		this.pass = pass;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	
	//태어난 해를 이용하여 현재의 나이를 반환하는 메소드는 직접 구현
	public int getAge() {
		int curyear = Calendar.getInstance().get(Calendar.YEAR);
		System.out.println(curyear);
		return curyear - year + 1;
	}
	
}
