import json, urllib, os, collections
import collections
import urllib.request
import shelve
from dreqPy import dreq

##
## fields returned by default (fields=*) (Oct 2023):
## ['_timestamp', '_version_', 'access', 'activity_drs', 'activity_id', 'cf_standard_name', 'citation_url', 'data_node', 'data_specs_version', 'dataset_id_template_', 'datetime_start', 'datetime_stop', 'directory_format_template_', 'experiment_id', 'experiment_title', 'frequency', 'further_info_url', 'grid', 'grid_label', 'id', 'index_node', 'instance_id', 'institution_id', 'latest', 'master_id', 'member_id', 'mip_era', 'model_cohort', 'nominal_resolution', 'number_of_aggregations', 'number_of_files', 'pid', 'product', 'project', 'realm', 'replica', 'retracted', 'score', 'size', 'source_id', 'source_type', 'sub_experiment_id', 'table_id', 'title', 'type', 'url', 'variable', 'variable_id', 'variable_long_name', 'variable_units', 'variant_label', 'version', 'xlink']

import localConfig

cv_dir = localConfig.config['directories']['cmip6_cvs']

e_id = json.load( open( '%s/CMIP6_experiment_id.json' % cv_dir, 'r' ) )['experiment_id']


class UrlOpenError(Exception):
    "Custom exception for errors in url library"
    pass

dq = dreq.loadDreq()

dr_map = dict()
dr_map0 = dict()

l1 = ['Lmon.mrro', 'Lmon.evspsblveg', 'Lmon.evspsblsoi', 'Amon.pr']
l2 = ['day.pr', 'day.tasmax','day.sfcWindmax','day.tasmin','day.clt']
dr_map_ex1 = set( [tuple(s.split('.')) for s in l1 + l2 ] )

temp_ex1 = 'https://%(esgf_node)s/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%%21=input4mips&table_id=%(table_label)s&mip_era=CMIP6&variable_id=%(variable_label)s&experiment_id=%(experiment_label)s&facets=mip_era%%2Cactivity_id%%2Cmodel_cohort%%2Cproduct%%2Csource_id%%2Cinstitution_id%%2Csource_type%%2Cnominal_resolution%%2Cexperiment_id%%2Csub_experiment_id%%2Cvariant_label%%2Cgrid_label%%2Ctable_id%%2Cfrequency%%2Crealm%%2Cvariable_id%%2Ccf_standard_name%%2Cdata_node&format=application%%2Fsolr%%2Bjson'

for i in dq.coll['CMORvar'].items:
    dr_map[ (i.mipTable,i.label) ] = i
    if (i.mipTable not in ['day','Amon']) and i.defaultPriority == 1:
        dr_map0[ (i.mipTable,i.label) ] = i

temp = 'https://%(esgf_node)s/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%%21=input4mips&activity_id=CMIP&table_id=%(table_label)s&mip_era=CMIP6&variable_id=%(variable_label)s&facets=mip_era%%2Cactivity_id%%2Cmodel_cohort%%2Cproduct%%2Csource_id%%2Cinstitution_id%%2Csource_type%%2Cnominal_resolution%%2Cexperiment_id%%2Csub_experiment_id%%2Cvariant_label%%2Cgrid_label%%2Ctable_id%%2Cfrequency%%2Crealm%%2Cvariable_id%%2Ccf_standard_name%%2Cdata_node&format=application%%2Fsolr%%2Bjson'

tempb = 'https://%(esgf_node)s/esg-search/search/?offset=%(offset)s&limit=10000&type=Dataset&replica=false&latest=true&activity_id=CMIP%(other_constraints)s&fields=%(return_fields)s&format=application%%2Fsolr%%2Bjson'
temp_base = 'https://%(esgf_node)s/esg-search/search/?'
tempb = 'offset=%(offset)s&limit=10000&type=Dataset&replica=false&latest=true%(other_constraints)s&fields=%(return_fields)s'
_format = '&format=' + urllib.parse.quote_plus('application/solr+json')

## http://esgf-data.dkrz.de/esg-search/search/?offset=0&limit=10&type=Dataset&replica=false&latest=true&experiment_id=historical&mip_era=CMIP6&activity_id%21=input4MIPs&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node

selection = "activity_id=CMIP&table_id=%(table_label)s&mip_era=CMIP6&variable_id=%(variable_label)s"
sdict = dict( table_id='Amon', experiment_id='historical', variable_id='tas' )

temp2 = 'https://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%%21=input4mips&%(selection)s&facets=mip_era%%2Cactivity_id%%2Cmodel_cohort%%2Cproduct%%2Csource_id%%2Cinstitution_id%%2Csource_type%%2Cnominal_resolution%%2Cexperiment_id%%2Csub_experiment_id%%2Cvariant_label%%2Cgrid_label%%2Ctable_id%%2Cfrequency%%2Crealm%%2Cvariable_id%%2Ccf_standard_name%%2Cdata_node&format=application%%2Fsolr%%2Bjson'

tmp = dict( Amon='tas, pr, uas, vas, huss, rsut, rsdt, rlut, rsus, rsds, rlus, rlds, ps, ua, va, zg, cl, clt'.split(', '),
            AERmon='od550aer, abs550aer'.split(', '),
            Lmon='cVeg, cLitter, gpp, nbp, npp'.split(', '),
            Omon=['fgco2',],
            Emon=['cSoil',],
            day='tas, pr, tasmax, tasmin'.split(', ')
           )

ifile = '../esgf_dashboard/cmip6-variables_gb_20220331.csv'
ifile = '../esgf_dashboard/cmip6-variables_04_09_2023.csv'

ee = {}

esgf_node = 'esgf-index1.ceda.ac.uk'
esgf_node = 'esgf-data.dkrz.de'

class Survey(object):
  def __init__(self,redo=False,return_after=-1,template=tempb):
      self.redo = redo
      self.return_after = return_after
      self.template = tempb

  def survey(self, shname, experiment_labels=['piControl']):
    esgf_node = 'esgf-index1.ceda.ac.uk'
    esgf_node = 'esgf-data.dkrz.de'
    sh = shelve.open( shname )
    _sh = shelve.open( '_' + shname )
    experiment_label = 'historical'
    return_fields = '*'
    return_fields = 'size%2Cid%2Cnumber_of_files' 
    _return_fields = 'size,id,number_of_files' 
    return_fields = urllib.parse.quote_plus( _return_fields )
    kk = 0
    for experiment_label in experiment_labels:
      this_key = experiment_label
      other_constraints = '&experiment_id=%(experiment_label)s&mip_era=CMIP6&variant_label=r1i1p1f1' % locals()
      other_constraints = '&experiment_id=%(experiment_label)s&mip_era=CMIP6' % locals()

      if self.redo or (this_key not in _sh.keys()):
      ##if variable_label in tmp[table_label]:
        try:
          complete = False
          offset = 0
          ntot =0
          sz = 0
          nf = 0
          kk = 0
          while not complete:
            kk+=1
            x =  temp_base % locals()
            y = self.template % locals() 
            u = x + y + _format
            obj = urllib.request.urlopen( u )
            ee = json.load( obj )
            for i in ee['response']['docs']:
                sz += i['size']
                nf += i['number_of_files']
                sh[ i['id'] ] = (i['size'],i['number_of_files'])
            ntot += len( ee['response']['docs'] )
            if ntot >= ee['response']['numFound']:
              complete = True
            else:
               offset += len( ee['response']['docs'] )
          print (experiment_label, int(sz*1.e-9), nf,kk,ntot)
          _sh[this_key] = (experiment_label, int(sz*1.e-9), nf,kk,ntot)

        except KeyboardInterrupt as e:
        ## if interrupted while reading, abondon this loop
          print("Caught keyboard interrupt [1]. Canceling tasks...")
          break
        ##except:
        ## if interrupted while reading, abondon this loop
          ####print("Exception raised while opening URL")
          ##raise UrlOpenError

      kk+=1
      if self.return_after > 0 and kk >= self.return_after: break

    sh.close()
    _sh.close()
    self.ee = ee
    return ee

    
def frank(l):
    r = l[-1]
    if l[-2] != None:
        r += 1.e-6*l[-2]
    else:
        r += 0.999
    return r
    
if __name__ == "__main__":
  op = 2.2
  if op == 2.2:
        s = Survey()
        dd = s.survey('esgf_cmip6_survey2b_dkrz_20231021',experiment_labels=sorted( list(e_id.keys()) ))
