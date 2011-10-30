#! /usr/bin/env python2
import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo

import dsa524

points = []
info1 = ""
tb = ""

GRID = 74
# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    def do_expose_event(self, event):
        """ expose() event """

        cr = self.window.cairo_create()
        # clip region
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()
        # call our draw function
        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # tube face is greeny-grey
        self.set_size_request(16 + GRID * 10, 16 + GRID * 8)
        cr.set_source_rgb(0.15, 0.25, 0.225)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        self.graticule(cr)
        

        
        self.trace(cr, points)   

    def graticule(self, cr):
        """ Draw a graticule, possibly after the waveform """
        cr.identity_matrix()
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.set_line_width(1);
        
        for i in range(0, 9*GRID, GRID):
            cr.move_to(8.5, i + 8.5)        
            cr.rel_line_to(10 * GRID, 0)
            cr.stroke()

        for i in range(0, 11*GRID, GRID):
            cr.move_to(i + 8.5, 8.5)        
            cr.rel_line_to(0, 8 * GRID)
            cr.stroke()
            
        cr.move_to(8.5, 8 + 4*GRID)
        cr.rel_line_to(10 * GRID, 0)
        cr.stroke()
        cr.move_to(8 + 5*GRID, 8.5)
        cr.rel_line_to(0, 8 * GRID)
        cr.stroke()

    def trace(self, cr, points):
        """ Draw an oscilloscope trace """

        cr.set_source_rgb(0.5, 1.0, 0.6) # green trace colour
        
        # to save time, make the bottom left corner be the origin
        # and make the top right corner be 1024,256 which matches
        # with what the DSA524 draws on
        
        cr.translate(8.5, 8.5 + GRID * 8)
        cr.scale(1/(1024.0 / 10 / GRID), -1/(256.0 / 8 / GRID))
        cr.move_to(0, 0);
        cr.set_line_width(2);

        #cr.move_to(0, points[0]);
        oy = points[0]
        x = 0        
        for y in points:
            cr.move_to(x-1, oy)
            cr.line_to(x, y)
            oy=y
            x = x+1
            cr.stroke()
        cr.identity_matrix()
        cr.select_font_face("Mono")
        cr.set_font_size(11)
        cr.move_to(12, 20)
        cr.show_text(info1)
        cr.move_to(12, 32)
        cr.show_text(tb)
    
# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def run(Widget, points):
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    
    
    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

if __name__ == "__main__":

    d = dsa524.DSA()
    d.connect()
    p = d.command("MEM?,TRA")
    p = p.split(",")
   
    i = d.command("CH1?")
    i = i.split(",")
    
    info1 = "CH1 %s/div %s-coupled" % (i[2], i[3]) 
    
    i = d.command("TMB?")
    i = i.split(",")
    tb = i[1:-1]
    tb = ", ".join(tb)
    tb = "%s/div" % i[1]
    print tb
    

    for i in p[:-1]:
        points.append(eval("0x"+i))
    
    run(Screen, points)
    
    
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
