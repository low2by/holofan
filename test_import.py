from encoder_test import Encoder

def main():
	encoder = Encoder();
	while(1):
		print encoder.readpos();
	
if __name__ == "__main__":
	main()
