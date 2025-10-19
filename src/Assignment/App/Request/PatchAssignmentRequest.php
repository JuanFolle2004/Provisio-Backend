<?php

declare(strict_types=1);

namespace Src\Assignment\App\Request;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Src\Assignment\Domain\Dtos\PatchAssignDto;
use Src\Assignment\Domain\Model\Assignment;

class PatchAssignmentRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'assignment_id'=>['required', 'integer', Rule::exists(Assignment::class, 'id')],
            'amount' => ['required', 'integer', 'min:1'],
            'bought'=>['required', 'integer', 'min:1', 'lte:amount'],
        ];
    }

    public function toDto(): PatchAssignDto
    {
        return new PatchAssignDto(
            assignmentId: $this->integer('assignment_id'),
            amount: $this->integer('amount'),
            bought: $this->integer('bought'),
        );
    }
}
