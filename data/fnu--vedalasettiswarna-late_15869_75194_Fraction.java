


public class Fraction {
	
		public int nume,deno,res_N,res_D;
		public StringBuffer ab=new StringBuffer();
		public Fraction(int i, int j) 
		{
			this.nume=i;
			this.deno=j;
		}
		public String add(Fraction f2){
			res_N=this.nume*f2.deno+this.deno*f2.nume;
			res_D=this.deno*f2.deno;
			String res=(ab.append(res_N).append("/").append(res_D)).toString();
			return(res);}
		public String sub(Fraction f2) {
			res_N=this.nume*f2.deno-this.deno*f2.nume;
			res_D=this.deno*f2.deno;
			String res=(ab.append(res_N).append("/").append(res_D)).toString();
			return(res);}
		public String mult(Fraction f2) {
			res_N=this.nume*f2.nume;
			res_D=this.deno*f2.deno;
			String res=(ab.append(res_N).append("/").append(res_D)).toString();
			return(res);}
		public String neg() {
			if(this.nume<0 && this.deno>0){
				this.nume=(this.nume)*-1;
				String res=(ab.append(this.nume).append("/").append(this.deno)).toString();
				return(res);}
			else if(this.deno<0 && this.nume>0){
				this.deno=this.deno*-1;
				String res=(ab.append(this.nume).append("/").append(this.deno)).toString();
				return(res);}
			else{
				String res=(ab.append(this.nume).append("/").append(this.deno)).toString();
				return(res);}
			}
	}



