void setup() {
  size(600,400);
}

float x = 0, y = 0, dx = 2.1, dy = 3.2;
void draw() {
  background(0);
   rect(x,y,100,100);
   x+= dx; y+= dy;
   if (x < 0 || x >= width)
     dx = -dx;
   if (y < 0 || y >= height)
     dy = -dy;
}