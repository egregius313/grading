
public class Fraction {
	private int num, den;
	private int gcf;
	private static int gcd(int a, int b) {
		if (b==0)
			return a;
		return gcd(b, a%b);
	}
	private void simplify() {
		gcf = gcd(num, den);
		if (gcf<0)
			gcf= -gcf;
		num /= gcf;
		den /= gcf;
	}
	public Fraction (int n, int d) {
		num = n;
		den = d;
		simplify();
		if (den < 0) {
			num = num*(-1);
			den = den*(-1);
		}
	}
	public Fraction(int n) {
		num = n;
		den = 1;
	}
	public Fraction() {
		num = 0;
		den = 1;
	}
	public Fraction add(Fraction right) {
		Fraction ans = new Fraction (this.num*right.den+right.num*this.den,this.den*right.den);
		return ans;
	}
	public Fraction sub(Fraction right) {
		Fraction ans = new Fraction (this.num*right.den-right.num*this.den,this.den*right.den);
		return ans;
	}
	public Fraction mult(Fraction right) {
		Fraction ans = new Fraction (this.num*right.num,this.den*right.den);
		simplify();
		return ans;
	}
	public Fraction neg() {
		Fraction ans = new Fraction (num*(-1),den);
		if (den < 0) {
			num = num*(-1);
			den = den*(-1);
			return ans;
		}
		return ans;
	}
	public void print() {
		System.out.println(num + "/" + den);
	}
	public String toString() {
		return num + "/" + den;
	}
	
	public static void main(String[] args) {
		for (int i = 1; i < 3; i++) {
			Fraction f1 = new Fraction(i,2);
			Fraction f2 = new Fraction(i,3);
			//System.out.println(f1);
			//System.out.println(f2);
			System.out.println(f1.add(f2));  // f1+f2
			System.out.println(f1.sub(f2));  // f1-f2
			System.out.println(f1.mult(f2)); // f1*f2
			System.out.println(f1.neg());    // -f1
			System.out.println(f2.neg());    // -f2
			System.out.println();
		}
		// Simplification Test
		// 1/2 + 1/2 should print 1/1, not 4/4.  See gcd in the example
		// from class
		System.out.println(new Fraction(2,2).add(new Fraction(2,5)));

		// should print 1/1
		System.out.println(new Fraction(1,8).mult(new Fraction(2,1)));
	}
}
