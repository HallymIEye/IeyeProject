<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<% 
	request.setCharacterEncoding("utf-8"); 
%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title> I-eye </title>
    <link href=infoboardcss.css rel=stylesheet type="text/css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-
    Mcw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css" />
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">&nbsp;&nbsp;I-Eye</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navBarSupportedContent" aria-expanded="false" 
    aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a class="nav-link" href="index.html">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="intro.html">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I-Eye 소개</a>
            </li>
            <li class="nav-item active">
                <a class="nav-link" href="download.html">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;OCT 다운로드</a>
                </li>
                <li class="nav-item active">
                    <a class="nav-link" href="close.html">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;주변 안과</a>
                    </li>
                    <li class="nav-item active">
                        <a class="nav-link" href="listboard.jsp">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;최신 소식</a>
                        </li>

                    </ul>
                    <form class="form-inline my-2 my-lg-0">
                      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                    </div>
                    </nav>
                    <br>
<div class="boardhelp">
 <div class="text-center">
<h2><a href="listboard.jsp" style="color:black;">자유 게시판</a> / <a href="infoboard2.html" style="color:black;">정보 사이트</a></h2>
<hr>


	<%@ page import="java.util.ArrayList, univ.BoardEntity, java.text.SimpleDateFormat" %>
	<jsp:useBean id="brddb" class="univ.BoardDBCP" scope="page" />
	<% 
		
		ArrayList<BoardEntity> list = brddb.getBoardList(); 
	   	int counter = list.size();
	   	int row = 0;
	   	
	   	if (counter > 0) {
	%>
<div class="container">
    <table class="table table-hover" >
    
    <tr bgcolor="lightgray">
       <th align=center>&nbsp;&nbsp;&nbsp;번호</th>
       <th align=center>제목</th>
       <th align=center>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;작성자</th>
       <th align=center>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;작성일</th>
       <th align=center>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;전자메일</th>
    </tr>
    
	<%
		
		SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		for( BoardEntity brd : list ) {
			
			String color = "gray";
			if ( ++row % 2 == 0 ) color = "white"; 
	%>
    <tr>
		<!-- 수정과 삭제를 위한 링크로 id를 전송 -->
       <td align=center><a href="editboard.jsp?id=<%= brd.getId()%>"><%= brd.getId()%></a></td>
       <td align=left><a href="editboard.jsp?id=<%= brd.getId()%>" style="color:black;"><%= brd.getTitle() %></a></td>
       <td align=center><%= brd.getName() %></td>
		
       <td align=center><%= df.format(brd.getRegdate()) %></td>
       <td align=center><%= brd.getEmail() %></td>
    </tr>
	<%
	    }
	%>
	</table>
<% 	}
%>
<hr width=90%>
<p>조회된 게시판 목록 수가 <%=counter%>개 입니다.

<hr>


<form name=form method=post action=editboard.jsp>
      <input class="btn btn-default pull-left" type=submit value="게시등록"> 
</form>

</div>
<div class="text-center">
<ul class="pagination">
<li><a href="#">1</a></li>
</ul>

</div>
</div>
</div>



        <div id=footer>
            <div id=logo2>
                    <a href="index.html"><img src="images/hallym3.png"></a>
            </div>
            
            <div id=info>
                <ul id=info1>
                <li>I eye 문의 010-8287-5573 | 031-513-5573</li> 
                <li>이메일주소 : ljjkms1@naver.com | 책임자 이용오 이지훈 신희철</li>
                <li>I eye CORPORATION. ALL RIGHTS RESERVED.</li>
             </ul>
            </div>

            <div id=sns>
                
                <a href=https://www.facebook.com target="_blank"><i class="fab fa-facebook-square fa-3x"></i></a>&nbsp;&nbsp;&nbsp;
                <a href=https://www.twitter.com target="_blank"><i class="fab fa-twitter-square fa-3x"></i></a>&nbsp;&nbsp;&nbsp;
                <a href=https://www.youtube.com target="_blank"><i class="fab fa-youtube-square fa-3x"></i></a>&nbsp;&nbsp;&nbsp;
                <a href=https://www.instargram.com target="_blank"><i class="fab fa-instagram fa-3x"></i></a>&nbsp;&nbsp;&nbsp;
                <a href=https://www.hallym.ac.kr target="_blank"><i class="fas fa-university fa-3x"></i></a>&nbsp;&nbsp;&nbsp;
                <a href=http://www.pask.or.kr/b_pask/index.php target="_blank" target="_blank"><i class="fas fa-camera fa-3x"></i></a>

            </div>



        </div>
            
                
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
                <script type="text/javascript" src="js/bootstrap.js"></script>
                                     <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
                <script type="text/javascript" src="js/bootstrap.js"></script>
                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/wow/1.1.2/wow.js"></script>
                <script>
                  var wow = new WOW(
                    {
                      boxClass: 'wow',
                      animateClass: 'animated',
                      offset: 0,
                      mobile: true,
                      live: true,
                      callback: function(box) {

                      },
                      scrollContainer: null,
                      resetAnimation: true,
                                          }
                  );
                  wow.init();
                  </script>
            </body>
            
            </html>
