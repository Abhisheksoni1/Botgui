<?php 
//$to='nilanjan.banerjee0@gmail.com';
$subject="Enquiry";
$headers = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type:text/html; charset=utf-8" . "\r\n";
$headers .= "From:contact@test.com\r\n";


$message='<table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0" style="font-family:Verdana, Arial, Helvetica, sans-serif;color:#000066" align="left">
        <tr>
          <td colspan="2" align="center" ><b><font color="#FFFFFF">Your Form Details</font></b></td>
        </tr>
        <tr bgcolor="#FFFFFF">
          <td style="font-size:11px; border-top:1px solid #333333; padding:10px;"><b>Dear &nbsp;User,</b></td>
        </tr>
        <tr bgcolor="#FFFFFF" align="left" >
          <td style="font-size:11px; border-top:1px solid #333333; padding:10px;">Information Details</td>
        </tr>
        <tr bgcolor="#FFFFFF" align="left">
          <td style="font-size:11px; border-top:1px solid #333333; padding:5px; line-height:18px;">
		  	<b> Name:</b>&nbsp;'.$_REQUEST['name'].'<br>
            <b> Email:</b>&nbsp;'.$_REQUEST['email'].'<br>
			
            <b> Messsage:</b>&nbsp;'.$_REQUEST['comments'].'<br>
        </tr>
        <tr>
          <td>&nbsp;</td>
        </tr>
        <tr> </tr>
      </table></td>
  </tr>
</table>';


if(mail($to, $subject, $message, $headers,'-f noreply@example.com'))
{
echo "<script>window.location='index.html?val=2'</script>";
}
else
{
echo "<script>window.location='index.html?val=3'</script>";
} 

?>