# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schemas which get wrapped by serializers."""
# TODO: remove the following lines after moving to python3.9
# allow `list[dict]` annotation, works without future-import for python>=3.9
from __future__ import annotations

import re

import arrow
from flask import current_app
from flask_resources import BaseObjectSchema
from invenio_rdm_records.resources.serializers.datacite.schema import (
    get_scheme_datacite,
)
from invenio_rdm_records.resources.serializers.ui.fields import AccessStatusField
from invenio_rdm_records.resources.serializers.ui.schema import (
    FormatDate,
    record_version,
)
from marshmallow import Schema, fields, missing
from marshmallow_oneofschema import OneOfSchema
from werkzeug.local import LocalProxy

from ...records import LOMRecord
from ...services.schemas.fields import ControlledVocabularyField


def get_text(value):
    """Get text from langstring object."""
    return value["langstring"]["#text"]


def get_lang(value):
    """Get lang from langstring object."""
    return value["langstring"]["lang"]


def get_related(obj: dict, relation_kind: str, catalog: str = "repo-pid") -> list:
    """Get dereferenced records that are `relation_kind`-related to `obj`."""
    results = []
    for relation in obj["metadata"].get("relation", []):
        if get_text(relation["kind"]["value"]) != relation_kind:
            continue

        for identifier in relation["resource"]["identifier"]:
            if identifier["catalog"] != catalog:
                continue

            results.append(identifier)

    return results


def get_newest_part(obj: dict):
    """."""
    parts = get_related(obj, relation_kind="haspart")
    return parts[-1]


class Title(fields.Field):
    """Title Field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""
        # TODO
        # checkout how to get the actual preferred language and show that string if it exists!
        return get_text(value)


class Contributors(fields.Field):
    """Contributors Field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""
        contributors = []
        for sub_obj in value:
            contributors.append(
                {
                    "fullname": sub_obj["entity"],
                    "role": get_text(sub_obj["role"]["value"]),
                }
            )
        return contributors


class GeneralDescriptions(fields.Field):
    """General Descriptions Field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""
        return list(map(get_text, value))


class EducationalDescriptions(fields.Field):
    """Educational Descriptions Field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""
        return list(map(get_text, value))


class Location(fields.Field):
    """Location Field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""
        return value["#text"]


class Rights(fields.Field):
    """Rights Field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""
        right = {}
        value = value or {}

        if "creativecommons" in value.get("url", ""):
            result = re.search("licenses/([a-z-]+)/.*", value["url"])
            id_ = f"CC {result.group(1).upper()}"
            icon = f"{id_.lower().replace(' ', '-')}-icon"
            right = {
                "id": id_,
                "title_l10n": id_,
                "description_l10n": id_,
                "link": value["url"],
                "icon": icon,
            }

        return [right]


class LOMUIBaseSchema(BaseObjectSchema):
    """Base schema for LOMUI-classes, containing all common fields."""

    created_date_l10n_long = FormatDate(attribute="created", format="long")

    updated_date_l10n_long = FormatDate(attribute="updated", format="long")

    resource_type = ControlledVocabularyField(
        attribute="resource_type",
        vocabulary=LocalProxy(lambda: current_app.config["LOM_RESOURCE_TYPES"]),
    )

    access_status = AccessStatusField(attribute="access")

    version = fields.Function(record_version)

    title = Title(attribute="metadata.general.title")

    location = Location(attribute="metadata.technical.location")

    rights = Rights(attribute="metadata.rights")

    is_draft = fields.Boolean(attribute="is_draft")

    contributors = fields.Method("get_contributors")

    generalDescriptions = fields.Method("get_general_descriptions")

    educationalDescriptions = fields.Method("get_educational_descriptions")

    def get_contributors(self, obj: dict):
        """Get contributors."""
        ui_contributors = []
        for lom_contribute in (
            obj["metadata"].get("lifecycle", {}).get("contribute", [])
        ):
            for entity in lom_contribute.get("entity", []):
                ui_contributors.append(
                    {
                        "fullname": entity,
                        "role": get_text(lom_contribute["role"]["value"]),
                    }
                )
        return ui_contributors

    def get_general_descriptions(self, obj: dict):
        """Get general descriptions."""
        return [
            get_text(desc)
            for desc in obj["metadata"].get("general", {}).get("description", [])
            if get_text(desc)
        ]

    def get_educational_descriptions(self, obj: dict):
        """Get educational descriptions."""
        return [
            get_text(desc)
            for desc in obj["metadata"].get("educational", {}).get("description", [])
            if get_text(desc)
        ]


class LOMUILinkSchema(LOMUIBaseSchema):
    """Schema for dumping html-template data to a record of resource_type "link"."""


class LOMUIFileSchema(LOMUIBaseSchema):
    """Schema for dumping html-template data to a record of resource_type "file"."""


class LOMUIUnitSchema(LOMUIBaseSchema):
    """Schema for dumping html-template data to a record of resource_type "unit"."""


class LOMUICourseSchema(LOMUIBaseSchema):
    """Schema for dumping html-template data to a record of resource_type "course"."""

    def get_contributors(self, obj: dict):
        """Get contributors, overwrites parent-class's `get_contributors`."""
        ui_contributors = []
        for unit in get_related(obj, relation_kind="haspart"):
            ui_contributors.extend(super().get_contributors(unit))

        return ui_contributors

    def get_general_descriptions(self, obj: dict):
        """Get general descriptions, overwrite parent-class's `get_general_descriptions`."""
        newest_unit = get_newest_part(obj)
        return super().get_general_descriptions(newest_unit)

    def get_educational_descriptions(self, obj: dict):
        """Get educational descriptions, overwrite parent-class's `get_educational_descriptions`."""
        newest_unit = get_newest_part(obj)
        return super().get_educational_descriptions(newest_unit)


class LOMUIUploadSchema(LOMUIFileSchema):
    """Schema for dumping html-template data to a record of resource_type "upload"."""


class LOMUIRecordSchema(OneOfSchema):
    """Delegates to different schemas depending on data_to_serialize["resource_type"]."""

    type_field = "resource_type"
    type_schemas = {
        "file": LOMUIFileSchema,
        "unit": LOMUIUnitSchema,
        "course": LOMUICourseSchema,
        "link": LOMUILinkSchema,
        "upload": LOMUIUploadSchema,
    }

    def get_obj_type(self, obj):
        """Get type of `obj`, which is used as a key to look up a schema within type_schemas."""
        return obj["resource_type"]


class LOMToDataCite44Schema(Schema):
    """Schema for conversion from LOM to DataCite-REST JSON 4.4."""

    identifiers = fields.Method("get_identifiers")
    creators = fields.Method("get_creators")
    titles = fields.Method("get_titles")
    publisher = fields.Method("get_publisher")
    publicationYear = fields.Method("get_publicationYear")
    types = fields.Constant(
        {
            "resourceType": "Educational Resource",
            "resourceTypeGeneral": "Other",
        }
    )

    contributors = fields.Method("get_contributors")
    dates = fields.Method("get_dates")
    language = fields.Method("get_language")
    relatedIdentifiers = fields.Method("get_relatedIdentifiers")
    sizes = fields.Method("get_sizes")
    formats = fields.Method("get_formats")
    version = fields.Method("get_version")
    rightsList = fields.Method("get_rightsList")

    schemaVersion = fields.Constant("http://datacite.org/schema/kernel-4")

    def get_identifiers(self, obj: LOMRecord):
        """Get list of (main and alternate) identifiers."""
        serialized_identifiers = []

        # identifiers from 'pids'-key, goes first so DOI gets included
        for scheme, pid_info in obj["pids"].items():
            serialized_identifiers.append(
                {
                    "identifier": pid_info["identifier"],  # e.g. 10.1234/foo
                    "identifierType": scheme.upper(),  # e.g. 'DOI', 'ISBN'
                }
            )

        # identifiers from LOM-metadata
        for lom_identifier in obj["metadata"].get("general", {}).get("identifier", []):
            identifier = lom_identifier.get("entry")
            identifier_type = lom_identifier.get("catalog")
            serialized_identifier = {
                "identifier": get_text(identifier),
                "identifierType": identifier_type.upper(),
            }
            if serialized_identifier not in serialized_identifiers:
                serialized_identifiers.append(serialized_identifier)

        return serialized_identifiers

    def get_creators(self, obj: LOMRecord):
        """Get list of creator-dicts."""
        contributes = obj["metadata"].get("lifecycle", {}).get("contribute", [])
        entities = []
        for contribute in contributes:
            entities.extend(contribute.get("entity", []))
        return [{"name": entity} for entity in entities]

    def get_titles(self, obj: LOMRecord):
        """Get list of title-dicts."""
        title = obj["metadata"].get("general", {}).get("title", None)
        if title is None:
            return []
        return [{"title": get_text(title), "lang": get_lang(title)}]

    def get_publisher(self, obj: LOMRecord):  # pylint: disable=unused-argument
        """Get publisher."""
        return current_app.config["LOM_PUBLISHER"]

    def get_publicationYear(self, obj: LOMRecord):
        """Get publication year."""
        contributes = obj["metadata"].get("lifecycle", {}).get("contribute", [])
        publish_dates = []
        for contribute in contributes:
            role = (
                contribute.get("role", {})
                .get("value", {})
                .get("langstring", {})
                .get("#text", "")
            )
            if role.lower() == "publisher":
                if publish_date := contribute.get("date", {}).get("dateTime"):
                    publish_dates.append(publish_date)

        if publish_dates:
            year = min(arrow.get(publish_date).year for publish_date in publish_dates)
        else:
            # from datacite specification: "For resources that do not have a standard publication year value, DataCite recommends that PublicationYear should include the date that is preferred for use in a citation."
            year = arrow.now().year

        return str(year)

    def get_contributors(self, obj: LOMRecord):
        """Get list of contributor-dicts."""
        contributes = obj["metadata"].get("lifeCycle", {}).get("contribute", [])
        contributors: list[dict[str, str]] = []
        for contribute in contributes:
            for entity in contribute.get("entity", []):
                contributor = {
                    "contributorType": "Other",
                    "name": entity,
                }
                contributors.append(contributor)
        return contributors or missing

    def get_dates(self, obj: LOMRecord):
        """Get list of date-dicts."""
        contributes = obj["metadata"].get("lifeCycle", {}).get("contribute", [])
        creator_dates = []

        for contribute in contributes:
            if date := contribute.get("date", {}).get("dateTime"):
                creator_dates.append(arrow.get(date))

        if not creator_dates:
            return missing

        first_date = min(creator_dates)  # first date some part of this was created
        last_date = max(creator_dates)  # last date some part of this was worked on
        if first_date == last_date:
            date = str(first_date.date())
        else:
            date = f"{first_date.date()}/{last_date.date()}"
        return [{"date": date, "dateType": "Created"}]

    def get_language(self, obj: LOMRecord):
        """Get language."""
        languages = obj["metadata"].get("general", {}).get("language", [])
        # LOM allows the special value "none" as language, but datacite does not
        languages = [lang for lang in languages if lang != "none"]
        if languages:
            return languages[0]
        return missing

    def get_relatedIdentifiers(self, obj: LOMRecord):
        """Get list of relatedIdentifier-dicts."""
        kind_to_relationType = {
            "ispartof": "IsPartOf",
            "haspart": "HasPart",
            "isversionof": "IsVersionOf",
            "hasversion": "HasVersion",
            "references": "References",
            "isreferencedby": "IsReferencedBy",
            "requires": "Requires",
            "isrequiredby": "IsRequiredBy",
            "isformatof": "IsDescribedBy",
            "hasformat": "Describes",
            "isbasedon": "IsDerivedFrom",
            "isbasisfor": "IsSourceOf",
        }
        relations = obj["metadata"].get("relation", [])
        relationdicts = []
        for relation in relations:
            identifiers = relation.get("resource", {}).get("identifier", [])
            kind_langstring = relation.get("kind", {}).get("value")
            if not kind_langstring:
                continue
            for identifier in identifiers:
                scheme = identifier.get("catalog", "").lower()
                # turn scheme into datacite-compatible type (corrects capitalization)
                id_type = get_scheme_datacite(scheme, "RDM_RECORDS_IDENTIFIERS_SCHEMES")
                if not id_type:
                    continue
                relationdicts.append(
                    {
                        "relatedIdentifier": get_text(identifier["entry"]),
                        "relatedIdentifierType": id_type,
                        "relationType": kind_to_relationType[get_text(kind_langstring)],
                    }
                )
        return relationdicts or missing

    def get_sizes(self, obj: LOMRecord):
        """Get list of sizes."""
        if size := obj["metadata"].get("technical", {}).get("size"):
            return [str(size)]
        return missing

    def get_formats(self, obj: LOMRecord):
        """Get list of formats."""
        return obj["metadata"].get("technical", {}).get("format", missing)

    def get_version(self, obj: LOMRecord):
        """Get version."""
        version_langstring = obj["metadata"].get("lifeCycle", {}).get("version", {})
        return version_langstring.get("langstring", {}).get("#text", missing)

    def get_rightsList(self, obj: LOMRecord):
        """Get list of rights-dicts."""
        rights = obj["metadata"].get("rights", {})
        if description_langstring := rights.get("description"):
            return [{"rights": get_text(description_langstring)}]
        return missing
