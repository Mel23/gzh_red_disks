#! /usr/bin/env python
import argparse
from astropy.table import Table,MaskedColumn,Column,hstack,vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.vizier import Vizier
from collections import OrderedDict
import numpy as np

def query(coords,catalog,cols,radius=2*u.arcsec,fill_val=-99.99,full=False):

    results = Vizier.query_region(coords,catalog=catalog,radius=radius)
    if len(results) == 0:
        return None

    if full:
        return results

    results = results[0]
    
    # if dict, remap colnames
    if isinstance(cols,dict):
        for k,v in cols.iteritems():
            results.rename_column(k,v)
        names = cols.values()
    else:
        names = cols

    # make new columns one-to-one with coords
    newtable = Table(masked=True)
    for col in names:
        oldcol = results[col]
        newcol = MaskedColumn(data=np.zeros(len(coords),dtype=oldcol.dtype),unit=oldcol.unit,name=col,mask=np.ones(len(coords),dtype=bool),fill_value=fill_val)

        # copy data from results
        for row in results:
            if not row[col]:
                continue
            # _q IS 1-BASED INDEXING?!
            newcol[row['_q']-1] = row[col]
            newcol.mask[row['_q']-1] = False

        newtable.add_column(newcol)

    return newtable



def main():
    parser = argparse.ArgumentParser(description='Query matches from vizier')
    parser.add_argument('table',type=str,help='Input table')
    parser.add_argument('-fmt',default='fits',help='Specify table format for astropy (default = fits')
    #parser.add_argument('cat',type=str,help='Catalog name on vizier')
    parser.add_argument('-rad',type=float,default=2,help='Search radius in arcsec (default = 2)')
    parser.add_argument('-o',type=str,help='If specified, output table')

    args = parser.parse_args()
    table = Table.read(args.table,format=args.fmt)
    coords = SkyCoord(ra=table['RA'],dec=table['DEC'],unit=(u.deg,u.deg))

    cat = 'II/312/ais'
    cols = ['FUV','e_FUV','NUV','e_NUV','objid','tile','img','sv']
            
    results = query(coords,cat,cols,args.rad*u.arcsec)
    if results is None:
        print 'No matches found'
        exit(1)
        
    table = hstack([table,results])
    table.pprint()
    if args.o:
        table.write(args.o,overwrite=True)


if __name__ == '__main__':
    main()
