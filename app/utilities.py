
import datetime
from app.models import Releases
from app import db
from sqlalchemy.sql.expression import nullslast
from sqlalchemy import desc

def get_latest_release(series):
	latest = Releases                                         \
				.query                                        \
				.filter(Releases.series==series.id)           \
				.filter(Releases.include==True)               \
				.order_by(nullslast(desc(Releases.volume)))   \
				.order_by(nullslast(desc(Releases.chapter)))  \
				.order_by(nullslast(desc(Releases.fragment))) \
				.limit(1)                                     \
				.scalar()

	return latest



def get_latest_releases(series_ids):

	query = Releases                                                               \
				.query                                                             \
				.with_entities(Releases.series, Releases.volume, Releases.chapter, Releases.fragment, Releases.published) \
				.order_by(Releases.series)                                         \
				.order_by(nullslast(desc(Releases.volume)))                        \
				.order_by(nullslast(desc(Releases.chapter)))                       \
				.order_by(nullslast(desc(Releases.fragment)))                      \
				.distinct(Releases.series)                                         \
				.filter(Releases.series.in_(series_ids))                           \
				.filter(Releases.include==True)

	latest = query.all()



	ret = {}
	for series, vol, chp, frag, pubdate in latest:
		if vol == None:
			vol = -1
		if chp == None:
			chp = -1
		if frag == None:
			frag = -1
		if series in ret:
			if vol > ret[series][0]:
				ret[series][0] = (vol, chp, frag)
			elif vol == ret[series][0] and chp > ret[series][1]:
				ret[series][0] = (vol, chp, frag)

			if ret[series][1] < pubdate:
				ret[series][1] = pubdate

		else:
			ret[series] = [(vol, chp, frag), pubdate]

	# Fill out any items which returned nothing.
	for sid in series_ids:
		if not sid in ret:
			ret[sid] = [(-1, -1, -1), None]

	return ret


def update_latest_row(series_row):
	db.session.flush()

	# print('update_latest_row')
	# print("Series row: ", series_row)

	maxpub = datetime.datetime.min
	releases = []

	# Proxy list because len(series_row.sqlalchemy_attr_thing) can fail.
	in_releases = list(series_row.releases)
	if not in_releases:
		return

	for release in in_releases:
		if release.include:
			releases.append((
					float(release.volume)   if release.volume   is not None else 0,
					float(release.chapter)  if release.chapter  is not None else 0,
					float(release.fragment) if release.fragment is not None else 0
				))
		if release.published > maxpub:
			maxpub = release.published

	releases.sort()

	if maxpub == datetime.datetime.min:
		maxpub = None

	if releases:
		vol, chp, frg = releases[-1]
	else:
		vol = None
		chp = None
		frg = None

	series_row.latest_published = maxpub
	series_row.latest_volume    = vol
	series_row.latest_chapter   = chp
	series_row.latest_fragment  = frg
	series_row.release_count    = len([tmp for tmp in series_row.releases if tmp.include])


