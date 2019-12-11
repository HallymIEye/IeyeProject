package univ;

import java.sql.*; 
import java.util.ArrayList; 

// �뀒�씠釉� student瑜� �쐞�븳 �뜲�씠�꽣踰좎씠�뒪 �뿰�룞 �옄諛붾퉰利� �봽濡쒓렇�옩
public class boarddatabase {

	// �뜲�씠�꽣踰좎씠�뒪 �뿰寃� 愿��젴 �긽�닔 �꽑�뼵
	private static final String JDBC_DRIVER = "org.gjt.mm.mysql.Driver";
	private static final String JDBC_URL = "jdbc:mysql://localhost:3306/univdb";
	private static final String USER = "root";
	private static final String PASSWD = "k1234";
	

	// �뜲�씠�꽣踰좎씠�뒪 �뿰寃� 愿��젴 蹂��닔 �꽑�뼵
	private Connection con = null;
	private Statement pstmt = null;

	// JDBC �뱶�씪�씠踰꾨�� 濡쒕뱶�븯�뒗 �깮�꽦�옄
	public boarddatabase() {
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
		if(pstmt != null) {
			try {
				pstmt.close();
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
	public ArrayList<BoardEntity> getBoardList() {	
		connect();
		ArrayList<BoardEntity> list = new ArrayList<BoardEntity>();
		
		String SQL = "select * from board";
		try {
			pstmt = con.prepareStatement(SQL);
			ResultSet rs = pstmt.executeQuery(SQL);
			
			while (rs.next()) {
				BoardEntity brd = new BoardEntity();
				brd.setId ( rs.getInt("id") );
				brd.setName ( rs.getString("name") );
				brd.setPasswd ( rs.getString("passwd") );
				brd.setTitle ( rs.getString("title") );
				brd.setEmail ( rs.getString("email") );
				brd.setRegdate ( rs.getTimestamp("regdate") );
				brd.setContent ( rs.getString("content") );
				//由ъ뒪�듃�뿉 異붽�
				list.add(brd);
			}
			rs.close();			
		} catch (SQLException e) {
			e.printStackTrace();
		} 
		finally {
			disconnect();
		}
		return list;
	}


}
