import os

from pywps import Process, LiteralInput, LiteralOutput

__author__ = 'Jonas Ziemer, Marlin Müller & Patrick Fischer'


class TempAlg(Process):
    def __init__(self):
        # inputs (basename, layername und expression)
        inputs = [LiteralInput('start1', 'Start date (eg. 2020-06-01)',
                               data_type='string'),
                  LiteralInput('end1', 'End date (eg. 2020-06-07)',
                               data_type='string'),
                  LiteralInput('start2', 'Start date (eg. 2020-06-01)',
                               data_type='string'),
                  LiteralInput('end2', 'End date (eg. 2020-06-07)',
                               data_type='string'),
                  ]
        outputs = [LiteralOutput('stats1', 'Computed STC-VH statistics',
                                 data_type='string'),
                   LiteralOutput('stats2', 'Computed STC-VV statistics',
                                 data_type='string')
                   ]

# Link for Execution!
# http://localhost:5000/wps?request=Execute&service=WPS&identifier=tempalg&version=1.0.0&datainputs=start1=2020-06-01;end1=2020-06-07;start2=2020-06-01;end2=2020-06-07

        super(TempAlg, self).__init__(
            self._handler,
            identifier='tempalg',
            version='0.1',
            title="Temporal Algorithms",
            abstract='Performs different aggregation algorithms and calculates univariate statistics in Sentinel-1-Space Time Cubes',
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
            grass_location="/home/user/Desktop/GRASSINEL_dir/grass_dir/GRASSINEL_test6"
        )

    def check_date(self, date_str):
        from datetime import datetime

        d = datetime.strptime(date_str, '%Y-%m-%d')
        if d.year != 2020:
            raise Exception("Only year 2020 allowed")

    def _handler(self, request, response):
        from subprocess import PIPE

        import grass.script as gs
        from grass.pygrass.modules import Module
        from grass.exceptions import CalledModuleError

        start1 = request.inputs['start1'][0].data
        end1 = request.inputs['end1'][0].data
        self.check_date(start1)
        self.check_date(end1)

        start2 = request.inputs['start2'][0].data
        end2 = request.inputs['end2'][0].data
        self.check_date(start2)
        self.check_date(end2)

        output1 = 'stcVH'
        output2 = 'stcVV'

        # be silent
        os.environ['GRASS_VERBOSE'] = '0'

        try:
            Module('t.rast.series',
                   input='stcubeVH@PERMANENT',
                   output=output1,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start1, end=end1
                   ))
            Module('t.rast.series',
                   input='stcubeVV@PERMANENT',
                   output=output2,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start2, end=end2
                   ))

        except CalledModuleError:
            raise Exception('Unable to compute statistics')

        ret = Module('r.univar',
                     flags='g',
                     map=output1,
                     stdout_=PIPE
                     )
        ret2 = Module('r.univar',
                      flags='g',
                      map=output2,
                      stdout_=PIPE
                      )
        stats1 = gs.parse_key_val(ret.outputs.stdout)
        stats2 = gs.parse_key_val(ret2.outputs.stdout)

        outstr1 = 'Min1: {0:.1f};Max1: {1:.1f};Mean1: {2:.1f}'.format(
            float(stats1['min']), float(stats1['max']), float(stats1['mean'])
        )
        outstr2 = 'Min2: {0:.1f};Max2: {1:.1f};Mean2: {2:.1f}'.format(
            float(stats2['min']), float(stats2['max']), float(stats2['mean'])
        )
        response.outputs['stats1'].data = outstr1
        response.outputs['stats2'].data = outstr2

        return response
