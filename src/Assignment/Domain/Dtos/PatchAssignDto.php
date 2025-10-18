<?php

declare(strict_types=1);

namespace Src\Assignment\Domain\Dtos;

class PatchAssignDto
{
    public function __construct(
        public readonly int $assignmentId,
        public readonly int $amount,
        public readonly int $bought,
    ) {
    }
}
