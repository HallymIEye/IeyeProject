package univ;

import java.sql.*; 
import java.util.ArrayList; 

// �뀒�씠釉� student瑜� �쐞�븳 �뜲�씠�꽣踰좎씠�뒪 �뿰�룞 �옄諛붾퉰利� �봽濡쒓렇�옩
public class StudentDatabase {

	// �뜲�씠�꽣踰좎씠�뒪 �뿰寃� 愿��젴 �긽�닔 �꽑�뼵
	private static final String JDBC_DRIVER = "org.gjt.mm.mysql.Driver";
	private static final String JDBC_URL = "jdbc:mysql://localhost:3306/univ";
	private static final String USER = "root";
	private static final String PASSWD = "k1234";

	// �뜲�씠�꽣踰좎씠�뒪 �뿰寃� 愿��젴 蹂��닔 �꽑�뼵
	private Connection con = null;
	private Statement stmt = null;

	// JDBC �뱶�씪�씠踰꾨�� 濡쒕뱶�븯�뒗 �깮�꽦�옄
	public StudentDatabase() {
		// JDBC �뱶�씪�씠踰� 濡쒕뱶
		try {
			Class.forName(JDBC_DRIVER);
		} catch (Exception e) {
			e.printStackTrace();
		}		
	}

	// �뜲�씠�꽣踰좎씠�뒪 �뿰寃� 硫붿냼�뱶
	public void connect() {
		try {
			// �뜲�씠�꽣踰좎씠�뒪�뿉 �뿰寃�, Connection 媛앹껜 ���옣 
			con = DriverManager.getConnection(JDBC_URL, USER, PASSWD);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// �뜲�씠�꽣踰좎씠�뒪 �뿰寃� �빐�젣 硫붿냼�뱶 
	public void disconnect() {
		if(stmt != null) {
			try {
				stmt.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		} 
		if(con != null) {
			try {
				con.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
	}

	// 寃뚯떆�뙋�쓽 紐⑤뱺 �젅肄붾뱶瑜� 諛섑솚�븯�뒗 硫붿냼�뱶
	public ArrayList<StudentEntity> getStudentList() {	
		connect();
		// 吏덉쓽 寃곌낵瑜� ���옣�븷 ArrayList瑜� �꽑�뼵
		// ArrayList �궡遺��뿉�뒗 �븰�깮�젙蹂대�� ���옣�븳 StudentEntity媛� �궫�엯
		ArrayList<StudentEntity> list = new ArrayList<StudentEntity>();

		String SQL = "select * from student";
		try {
			stmt = con.createStatement();
			ResultSet rs = stmt.executeQuery(SQL);

			//ResultSet�쓽 寃곌낵�뿉�꽌 紐⑤뱺 �뻾�쓣 媛곴컖�쓽 StudentEntity 媛앹껜�뿉 ���옣  
			while (rs.next()) {		
				//�븳 �뻾�쓽 �븰�깮�젙蹂대�� ���옣�븷 �븰�깮�쓣 �쐞�븳 鍮덉쫰 媛앹껜 �깮�꽦  
				StudentEntity stu = new StudentEntity();

				//�븳 �뻾�쓽 �븰�깮�젙蹂대�� �옄諛� 鍮덉쫰 媛앹껜�뿉 ���옣  				
				stu.setId ( rs.getString("id") );
				stu.setPasswd ( rs.getString("passwd") );
				stu.setName ( rs.getString("name") );
				stu.setYear ( rs.getInt("year") );
				stu.setSnum ( rs.getString("snum") );
				stu.setDepart ( rs.getString("depart") );
				stu.setMobile1 ( rs.getString("mobile1") );
				stu.setMobile2 ( rs.getString("mobile2") );
				stu.setAddress ( rs.getString("address") );
				stu.setEmail ( rs.getString("email") );
				//ArrayList�뿉 �븰�깮�젙蹂� StudentEntity 媛앹껜瑜� 異붽�
				list.add(stu);
			}
			rs.close();			
		} catch (SQLException e) {
			e.printStackTrace();
		} 
		finally {
			disconnect();
		}
		//�셿�꽦�맂 ArrayList 媛앹껜瑜� 諛섑솚
		return list;
	}

}
