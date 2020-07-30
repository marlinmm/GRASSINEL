import os

from pywps import Process, LiteralInput, LiteralOutput

__author__ = 'Martin Landa'


class TempAlg(Process):
    def __init__(self):
        # inputs (basename, layername und expression)
        inputs = [LiteralInput('start1', 'Start date (eg. 2019-03-01)',
                               data_type='string'),
                  LiteralInput('end1', 'End date (eg. 2019-04-01)',
                               data_type='string'),
                  LiteralInput('start2', 'Start date (eg. 2019-03-01)',
                               data_type='string'),
                  LiteralInput('end1', 'End date (eg. 2019-04-01)',
                               data_type='string'),
                  # LiteralInput('expression', 'Expression (eg. bla blubb)', data_type='string')
                  ]
        outputs = [LiteralOutput('stats', 'Computed LST statistics',
                                 data_type='string')
                   ]

        super(TempAlg, self).__init__(
            self._handler,
            identifier='tempalg',
            version='0.1',
            title="Temporal Algorithms",
            abstract='Temporal Algorithms for SpaceTimeCubes',
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
            grass_location="/home/user/Desktop/GEO450_main_dir/grass_dir/GEO450_test1"
        )

    def check_date(self, date_str):
        from datetime import datetime

        d = datetime.strptime(date_str, '%Y-%m-%d')
        if d.year != 2019:
            raise Exception("Only year 2019 allowed")

    def _handler(self, request, response):
        from subprocess import PIPE

        import grass.script as gs
        from grass.pygrass.modules import Module
        from grass.exceptions import CalledModuleError

        start = request.inputs['start'][0].data
        end = request.inputs['end'][0].data
        self.check_date(start)
        self.check_date(end)

        output1 = 'stcVH'
        output2 = 'stcVV'

        # be silent
        os.environ['GRASS_VERBOSE'] = '0'

        try:
            Module('t.rast.series',
                   input='stcVH@PERMANENT',
                   output=output1,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start, end=end
                   ))
            Module('t.rast.series',
                   input='stcVV@PERMANENT',
                   output=output2,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start, end=end
                   ))

        except CalledModuleError:
            raise Exception('Unable to compute statistics')

        ret = Module('r.univar',
                     flags='g',
                     map=output1,
                     stdout_=PIPE
                     )
        stats = gs.parse_key_val(ret.outputs.stdout)

        outstr = 'Min: {0:.1f};Max: {1:.1f};Mean: {2:.1f}'.format(
            float(stats['min']), float(stats['max']), float(stats['mean'])
        )
        response.outputs['stats'].data = outstr

        return response
