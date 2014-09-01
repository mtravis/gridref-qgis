# -*- coding: utf-8 -*-

# xy_to_osgb - A library of functions for converting eastings and 
# northings to OS Grid References
# Copyright (C) 2014 Peter Wells for Lutra Consulting

# peter dot wells at lutraconsulting dot co dot uk
# Lutra Consulting
# 23 Chestnut Close
# Burgess Hill
# West Sussex
# RH15 8HN

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

major_letters = {
    0 : {
        0 : 'S',
        1 : 'N',
        2 : 'H'
    },
    1 : {
        0 : 'T',
        1 : 'O'
    }
}

minor_letters = {
    0 : {
        0 : 'V', 1 : 'Q', 2 : 'L', 3 : 'F', 4 : 'A'
    },
    1 : {
        0 : 'W', 1 : 'R', 2 : 'M', 3 : 'G', 4 : 'B'
    },
    2 : {
        0 : 'X', 1 : 'S', 2 : 'N', 3 : 'H', 4 : 'C'
    },
    3 : {
        0 : 'Y', 1 : 'T', 2 : 'O', 3 : 'J', 4 : 'D'
    },
    4 : {
        0 : 'Z', 1 : 'U', 2 : 'P', 3 : 'K', 4 : 'E'
    }
}

supported_precisions = [1000, 100, 10, 1]

def xy_to_osgb(easting, northing, precision=1000):
    
    """
        
    """
    
    if not precision in supported_precisions:
        raise Exception('Precision of ' + str(precision) + ' is not supported.')
    
    # Determine first letter
    
    x_idx = easting // 500000
    y_idx = northing // 500000
    major_letter = major_letters[x_idx][y_idx]
    
    # Determine 'index' of 100km square within the larger 500km tile
    
    macro_easting = easting % 500000
    macro_northing = northing % 500000
    macro_x_idx = macro_easting // 100000
    macro_y_idx = macro_northing // 100000
    minor_letter = minor_letters[macro_x_idx][macro_y_idx]
    
    # determine the internal coordinate withing the 100km tile
    micro_easting = macro_easting % 100000
    micro_northing = macro_northing % 100000
    
    # determine how to report the numeric part
    ref_x = micro_easting // precision
    ref_y = micro_northing // precision
    
    coord_width = 2
    if precision == 100:
        coord_width = 3
    elif precision == 10:
        coord_width = 4
    elif precision == 1:
        coord_width = 5

    format_string = r'%s%s %0' + str(coord_width) + r'd %0' + str(coord_width) + r'd'
    return format_string % (major_letter, minor_letter, ref_x, ref_y)
    

def main():
    """ Unit test """
    assert xy_to_osgb(432574, 332567) == 'SK 32 32'
    assert xy_to_osgb(236336, 682945) == 'NS 36 82'
    assert xy_to_osgb(392876, 494743) == 'SD 92 94'
    assert xy_to_osgb(472945, 103830) == 'SU 72 03'
    
    assert xy_to_osgb(432574, 332567, 100) == 'SK 325 325'
    assert xy_to_osgb(236336, 682945, 100) == 'NS 363 829'
    assert xy_to_osgb(392876, 494743, 100) == 'SD 928 947'
    assert xy_to_osgb(472945, 103830, 100) == 'SU 729 038'
    
    assert xy_to_osgb(432574, 332567, 10) == 'SK 3257 3256'
    assert xy_to_osgb(236336, 682945, 10) == 'NS 3633 8294'
    assert xy_to_osgb(392876, 494743, 10) == 'SD 9287 9474'
    assert xy_to_osgb(472945, 103830, 10) == 'SU 7294 0383'
    
    assert xy_to_osgb(432574, 332567, 1) == 'SK 32574 32567'
    assert xy_to_osgb(236336, 682945, 1) == 'NS 36336 82945'
    assert xy_to_osgb(392876, 494743, 1) == 'SD 92876 94743'
    assert xy_to_osgb(472945, 103830, 1) == 'SU 72945 03830'
    

if __name__ == "__main__":
    main()
