use Net::TacacsPlus::Client;

my ($host, $key, $username, $password) = @ARGV;  
	
#my $host='14.141.47.12';

#my $key='asm-tacacs-plus';

my $result=tacacs_auth($host,$key,$username,$password);
print "\nResult : $result \n";

sub tacacs_auth()
{
	my ($host,$key,$username,$password) = @_;	
        my $tac = new Net::TacacsPlus::Client(host => $host, key => $key);

        if ($tac->authenticate($username, $password, 0x01))
	{                                                              
		return "pass";
	}	
	return "fail";	
}       
